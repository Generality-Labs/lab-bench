"""Solvers for the LAB-Bench 2 evaluation.

The reference benchmark runs each model in two configurations: `bare` (no tools,
single-turn) and an agentic configuration with provider-native tools. This package
groups the solver factories and the registry that maps a ``SolverType`` to them.
"""

from lab_bench_2.solvers.registry import (
    SOLVERS_BY_TYPE,
    SolverType,
    solver_for_type,
)
from lab_bench_2.solvers.solvers import bare, native_tools, tools

__all__ = [
    "SOLVERS_BY_TYPE",
    "SolverType",
    "bare",
    "native_tools",
    "solver_for_type",
    "tools",
]
