"""Registry mapping a ``SolverType`` to its solver factory."""

from __future__ import annotations

from typing import Literal

from inspect_ai.solver import Solver

from lab_bench_2.solvers.solvers import bare, tools

SolverType = Literal["bare", "tools"]

SOLVERS_BY_TYPE = {
    "bare": bare,
    "tools": tools,
}


def solver_for_type(solver_type: SolverType) -> Solver:
    """Return the solver for a type, or raise if the type is not yet implemented."""
    factory = SOLVERS_BY_TYPE.get(solver_type)
    if factory is None:
        raise NotImplementedError(
            f"No solver implemented for type={solver_type!r}; "
            f"supported types: {sorted(SOLVERS_BY_TYPE)}."
        )
    return factory()
