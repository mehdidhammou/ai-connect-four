from typing import Annotated, get_args

from fastapi import Path
from pydantic import TypeAdapter

from src.heuristic.heuristic_factory import HeuristicFactory
from src.model import ModelProviderFactory
from src.solver import MinimaxAlphaBetaPruningSolver
from src.solver.llm_based_solver import LLMBasedSolver
from src.types.model import Model
from src.types.model_provider_name import ModelProviderName
from src.types.solver_type import SolverType


def get_solver(solver_type: SolverType):
    if solver_type.type == "heuristic":
        heuristic = HeuristicFactory.create(name=solver_type.name)
        return MinimaxAlphaBetaPruningSolver(heuristic=heuristic, depth=4)

    elif solver_type.type in get_args(ModelProviderName):
        model_provider = ModelProviderFactory.create(solver_type.type)
        model = Model(name=solver_type.name)

        if model not in model_provider.get_models():
            raise ValueError(
                f"Model '{model.name}' not found in provider '{model_provider.name}'."
            )

        return LLMBasedSolver(
            model_provider=model_provider,
            model=model,
        )

    else:
        raise ValueError(f"Unknown solver type: {solver_type.type}")


def validate_solver_type(
    solver: Annotated[str, Path(...)],
    name: Annotated[str, Path(...)],
) -> SolverType:
    return TypeAdapter(SolverType).validate_python({"type": solver, "name": name})
