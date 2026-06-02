from typing import Any

from inspect_ai import Task, eval
from inspect_ai.dataset import Sample
from inspect_ai.model import ChatMessage, ModelOutput, get_model
from inspect_ai.solver import Solver

from lab_bench_2.solvers.agent import (
    FINAL_WARNING_MESSAGE,
    agent_with_final_warning,
    agentic,
)


def test_agentic_returns_solver() -> None:
    assert isinstance(agentic(), Solver)


def _never_submit_until_warned(
    messages: list[ChatMessage],
    tools: Any,
    tool_choice: Any,
    config: Any,
) -> ModelOutput:
    """Submit only once the final-warning prompt has been injected.

    Before the warning, the model returns plain content (no tool call), so the
    agent loops until it exhausts its message budget without submitting.
    """
    last_text = messages[-1].text if messages else ""
    if "MUST submit your answer NOW" in last_text:
        return ModelOutput.for_tool_call(
            model="mockllm/model",
            tool_name="submit",
            tool_arguments={"answer": "RECOVERED"},
        )
    return ModelOutput.from_content(
        model="mockllm/model", content="still working, no final answer yet"
    )


def test_final_warning_recovers_answer_when_model_never_submits() -> None:
    # given a model that only submits once the final-warning prompt is injected
    model = get_model("mockllm/model", custom_outputs=_never_submit_until_warned)
    task = Task(
        dataset=[Sample(input="What is the answer?", target="RECOVERED")],
        solver=agent_with_final_warning(warning_limit=4),
    )
    # when the agent runs out of turns without submitting
    log = eval(task, model=model)[0]
    # then the final-warning path recovers the submitted answer
    assert log.status == "success"
    assert log.samples is not None
    assert log.samples[0].output.completion == "RECOVERED"
    # and the warning was actually injected into the conversation
    assert any(FINAL_WARNING_MESSAGE in m.text for m in log.samples[0].messages)


def _dangling_submit(
    messages: list[ChatMessage],
    tools: Any,
    tool_choice: Any,
    config: Any,
) -> ModelOutput:
    """Emit a submit call that is cut off by the context window.

    With ``stop_reason="model_length"``, basic_agent breaks its loop without
    executing the tool, so the submit call is left dangling for the wrapper to
    resolve.
    """
    output = ModelOutput.for_tool_call(
        model="mockllm/model",
        tool_name="submit",
        tool_arguments={"answer": "DANGLED"},
    )
    output.choices[0].stop_reason = "model_length"
    return output


def test_recovers_dangling_submit_when_interrupted_mid_tool_call() -> None:
    # given a model whose submit call is cut off by the context window, so
    # basic_agent exits with the submit tool call still unresolved
    model = get_model("mockllm/model", custom_outputs=_dangling_submit)
    task = Task(
        dataset=[Sample(input="What is the answer?", target="DANGLED")],
        solver=agent_with_final_warning(warning_limit=50),
    )
    # when the wrapper resolves the dangling call
    log = eval(task, model=model)[0]
    # then the submit tool runs and its answer is recovered
    assert log.status == "success"
    assert log.samples is not None
    sample = log.samples[0]
    assert sample.output.completion == "DANGLED"
    # and recovery came from resolving the dangling call, not from the
    # final-warning fallback (which is never injected in this path)
    assert all(FINAL_WARNING_MESSAGE not in m.text for m in sample.messages)
