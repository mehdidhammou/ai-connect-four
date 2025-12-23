from pydantic import BaseModel
from src.types.move import Move
from src.types.solver_type import SolverType
from typing_extensions import Literal

from .board_request import Piece


class MoveRequest(BaseModel):
    board: list[list[Piece]]
    starting_player: Literal["human", "cpu"]
    player_move: Move
    player_piece: Piece
    solver_piece: Piece
    solver: SolverType
