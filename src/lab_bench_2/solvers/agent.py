"""Shared agentic solver with final-warning mechanism for LabBench2 tasks.

Wraps basic_agent with a message-limit-aware final-warning prompt that
forces the agent to submit before running out of time.
"""

from textwrap import dedent
from typing import Any

from inspect_ai.model import ChatMessageTool, ChatMessageUser, execute_tools, get_model
from inspect_ai.solver import Generate, Solver, TaskState, basic_agent, solver
from inspect_ai.util import LimitExceededError

RETRY_MESSAGE = dedent("""\
    Your last python() call was empty or malformed.
    Think step-by-step (<=2 lines) **then** emit a python(code: str) call for the SAME question.
    If the code would be >2000 chars, write it to sequence.json first and import from there.""")

FINAL_WARNING_MESSAGE = dedent("""\
    You are running out of time and MUST submit your answer NOW.
    Based on everything you have learned so far, use the submit()
    tool to submit your single best answer. Do NOT run any more
    code — just submit your best guess immediately.""")


@solver
def agent_with_final_warning(
    warning_limit: int = 45,
    **agent_kwargs: Any,
) -> Solver:
    """Wrap basic_agent with a final-warning mechanism.

    Runs basic_agent with a message_limit of `warning_limit`. If the agent
    hits that limit without submitting, injects a "submit NOW" prompt and
    gives the model one more generation with tools to submit its best guess.
    """
    agent_solver = basic_agent(message_limit=warning_limit, **agent_kwargs)

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        try:
            state = await agent_solver(state, generate)
        except LimitExceededError:
            pass  # Agent hit message limit without submitting — expected

        # Bump limit generously: room for dangling-tool resolution (2),
        # final-warning user message (1), model response (1), and tool
        # execution results (2).
        state.message_limit = len(state.messages) + 6

        # Resolve any dangling tool calls from the interrupted agent.
        if state.output and state.output.message.tool_calls:
            resolved_ids = {
                msg.tool_call_id
                for msg in state.messages
                if isinstance(msg, ChatMessageTool) and msg.tool_call_id
            }
            has_pending = any(
                tc.id not in resolved_ids for tc in state.output.message.tool_calls
            )
            if has_pending:
                tool_results, _ = await execute_tools(
                    [state.output.message], state.tools
                )
                state.messages.extend(tool_results)

        # Check if submit was already called (either normally or via dangling resolution)
        submitted = any(
            isinstance(msg, ChatMessageTool) and msg.function == "submit"
            for msg in state.messages
        )
        if submitted:
            for msg in reversed(state.messages):
                if isinstance(msg, ChatMessageTool) and msg.function == "submit":
                    state.output.completion = msg.text
                    break
            return state

        # Inject warning, one final generate
        state.messages.append(ChatMessageUser(content=FINAL_WARNING_MESSAGE))

        output = await get_model().generate(input=state.messages, tools=state.tools)
        state.messages.append(output.message)
        state.output = output

        if output.message.tool_calls:
            # Extract submit answer directly from tool call arguments so
            # the completion is captured even if execute_tools is blocked
            # by the message limit.
            for tc in output.message.tool_calls:
                if tc.function == "submit":
                    answer = (
                        tc.arguments.get("answer", "")
                        if isinstance(tc.arguments, dict)
                        else ""
                    )
                    state.output.completion = answer
                    break

            # Still execute the tools for proper message-state bookkeeping
            tool_results, _ = await execute_tools([output.message], state.tools)
            state.messages.extend(tool_results)

        return state

    return solve
