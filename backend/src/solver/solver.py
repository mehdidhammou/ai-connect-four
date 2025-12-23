from abc import ABC, abstractmethod

from src.board.connect_four_board import ConnectFourBoard
from src.types.move import Move
from src.types.piece_enum import PieceEnum


class Solver(ABC):
    @abstractmethod
    def solve(self, board: ConnectFourBoard, piece: PieceEnum) -> Move | None:
        pass
