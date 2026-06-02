from typing import cast

import pytest
from inspect_ai.solver import Solver

from lab_bench_2.solvers.registry import (
    SOLVERS_BY_TYPE,
    SolverType,
    solver_for_type,
)


class TestSolverForType:
    def test_bare_and_tools_are_registered(self) -> None:
        # given / when / then the supported types are exactly bare and tools
        assert set(SOLVERS_BY_TYPE) == {"bare", "tools"}

    def test_returns_a_solver_for_each_registered_type(self) -> None:
        # given each registered solver type
        # when / then a Solver instance is produced
        for solver_type in SOLVERS_BY_TYPE:
            assert isinstance(solver_for_type(cast(SolverType, solver_type)), Solver)

    def test_raises_for_unimplemented_type(self) -> None:
        # given a solver type that is not registered
        # when / then a NotImplementedError is raised
        with pytest.raises(NotImplementedError):
            solver_for_type(cast(SolverType, "nonexistent"))
