from typing import Annotated

from pydantic import BaseModel, Field
from src.types.heuristic_name import HeuristicName
from src.types.piece import Piece


class BoardRequest(BaseModel):
    board: list[list[Piece]]
    heuristic: HeuristicName
