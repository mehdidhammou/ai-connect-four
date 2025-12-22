from pydantic import BaseModel
from src.types.move import Move
from src.types.solver_type import SolverType

from .board_request import Piece


class MoveRequest(BaseModel):
    board: list[list[Piece]]
    player_move: Move
    player_piece: Piece
    solver_piece: Piece
    solver: SolverType
