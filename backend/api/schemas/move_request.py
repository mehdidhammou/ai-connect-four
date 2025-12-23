from pydantic import BaseModel
from src.types.move import Move
from src.types.piece_enum import PieceEnum
from src.types.solver_type import SolverType
from typing_extensions import Literal


class MoveRequest(BaseModel):
    board: list[list[PieceEnum]]
    starting_player: Literal["human", "cpu"]
    player_move: Move
    solver: SolverType
