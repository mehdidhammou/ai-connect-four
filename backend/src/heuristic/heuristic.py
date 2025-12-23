from typing import Protocol

from src.board.connect_four_board import ConnectFourBoard
from src.types.move import Move
from src.types.piece_enum import PieceEnum


class Heuristic(Protocol):
    @staticmethod
    def evaluate(board: ConnectFourBoard, piece: PieceEnum) -> float: ...

    @staticmethod
    def first_play() -> Move: ...
