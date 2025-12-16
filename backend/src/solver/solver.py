from abc import ABC, abstractmethod
from src.board.connect_four_board import ConnectFourBoard
from src.types.move import Move


class Solver(ABC):
    @abstractmethod
    def solve(self, board: ConnectFourBoard) -> Move:
        pass
