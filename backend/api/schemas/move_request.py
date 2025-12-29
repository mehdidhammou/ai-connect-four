from pydantic import BaseModel
from src.types.move import Move
from src.types.piece_enum import PieceEnum


class MoveRequest(BaseModel):
    board: list[list[PieceEnum]]
    player_move: Move
