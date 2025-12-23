from src.heuristic import HeuristicFactory
from src.model import ModelProviderFactory
from src.solver import MinimaxAlphaBetaPruningSolver
from src.solver.llm_based_solver import LLMBasedSolver
from src.types.solver_type import SolverType


def get_solver(solver_type: SolverType):
    if solver_type.type == "minimax_alpha_beta":
        heuristic = HeuristicFactory.create(name=solver_type.name)
        return MinimaxAlphaBetaPruningSolver(heuristic=heuristic, depth=4)

    elif solver_type.type == "llm":
        model_provider = ModelProviderFactory.create(solver_type.provider)
        return LLMBasedSolver(
            model_provider=model_provider, model_name=solver_type.name
        )

    else:
        raise ValueError(f"Unknown solver type: {solver_type}")
