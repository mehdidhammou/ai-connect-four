from pydantic import BaseModel, Field
from typing_extensions import Annotated, Literal, Union
from src.types.heuristic_name import HeuristicName

from .model_provider_name import ModelProviderName


class HeuristicSolverType(BaseModel):
    type: Literal["heuristic"]
    name: HeuristicName


class LLMSolverType(BaseModel):
    type: ModelProviderName
    name: str


SolverType = Annotated[
    Union[HeuristicSolverType, LLMSolverType], Field(discriminator="type")
]
