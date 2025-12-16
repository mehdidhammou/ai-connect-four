from abc import ABC, abstractmethod
from src.types.move import Move
from src.board.connect_four_board import ConnectFourBoard


class Heuristic(ABC):
    def __init__(self, id: int):
        self.id = id

    @abstractmethod
    def evaluate(self, board: ConnectFourBoard, piece: int) -> float:
        pass

    @abstractmethod
    def first_play(self) -> Move:
        pass
