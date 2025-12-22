from pydantic import BaseModel

from .move_request import SolverType
from src.types.piece import Piece


class AutoMoveRequest(BaseModel):
    board: list[list[Piece]]
    solver_one: SolverType
    solver_two: SolverType
    current_piece: Piece
