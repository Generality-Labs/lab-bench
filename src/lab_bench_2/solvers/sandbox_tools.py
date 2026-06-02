"""Tool helpers for LabBench2 agentic evaluations."""

from __future__ import annotations

import os

from inspect_ai.tool import Tool, bash, python, web_search


def _build_web_search() -> Tool | None:
    """Build web_search with an external provider.

    Internal providers (openai, anthropic, gemini) use the model's built-in
    search but cannot coexist with other tools like python() and bash()
    (Gemini raises "does not yet support native web search concurrently
    with other tools").  We use external-only providers so search works
    alongside code execution for every model.
    """
    if os.environ.get("TAVILY_API_KEY"):
        return web_search("tavily")
    if os.environ.get("EXA_API_KEY"):
        return web_search("exa")
    if os.environ.get("GOOGLE_CSE_API_KEY"):
        return web_search("google")
    return None


def get_labbench2_tools(timeout: int = 180) -> list[Tool]:
    """Return the standard LabBench2 tool set (python, bash, optionally web_search).

    web_search is included when an external provider key is configured
    (TAVILY_API_KEY, EXA_API_KEY, or GOOGLE_CSE_API_KEY).
    """
    tools: list[Tool] = [python(timeout=timeout), bash(timeout=timeout)]
    ws = _build_web_search()
    if ws is not None:
        tools.append(ws)
    return tools
