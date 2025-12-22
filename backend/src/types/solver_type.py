from pydantic import BaseModel
from typing_extensions import Literal
from .heuristic_enum import HeuristicEnum
from .model_provider_enum import ModelProviderEnum


class MinimaxSolver(BaseModel):
    type: Literal["minimax_alpha_beta"]
    name: HeuristicEnum


class LLMSolver(BaseModel):
    type: Literal["llm"]
    provider: ModelProviderEnum
    model_name: str


SolverType = MinimaxSolver | LLMSolver
