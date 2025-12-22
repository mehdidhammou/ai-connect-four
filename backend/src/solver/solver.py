from abc import ABC, abstractmethod

from src.board.connect_four_board import ConnectFourBoard
from src.types.move import Move
from src.types.piece import Piece


class Solver(ABC):
    @abstractmethod
    def solve(self, board: ConnectFourBoard, piece: Piece) -> Move | None:
        pass
