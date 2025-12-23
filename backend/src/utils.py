from typing import Annotated

from fastapi import Path
from pydantic import TypeAdapter

from src.heuristic import HeuristicFactory
from src.model import ModelProviderFactory
from src.solver import MinimaxAlphaBetaPruningSolver
from src.solver.llm_based_solver import LLMBasedSolver
from src.types.solver_type import SolverType


def get_solver(solver_type: SolverType):
    if solver_type.type == "heuristic":
        heuristic = HeuristicFactory.create(name=solver_type.name)
        return MinimaxAlphaBetaPruningSolver(heuristic=heuristic, depth=4)

    else:
        model_provider = ModelProviderFactory.create(solver_type.type)
        return LLMBasedSolver(
            model_provider=model_provider, model_name=solver_type.name
        )


def validate_solver_type(
    solver: Annotated[str, Path(...)],
    name: Annotated[str, Path(...)],
) -> SolverType:
    return TypeAdapter(SolverType).validate_python({"type": solver, "name": name})
