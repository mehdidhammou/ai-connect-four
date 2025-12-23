# abstract model provider class
from abc import ABC, abstractmethod

from src.board.connect_four_board import ConnectFourBoard
from src.types.piece_enum import PieceEnum
from src.types.move import Move

from .model import Model


class ModelProvider(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_models(self) -> list[Model]:
        pass

    @abstractmethod
    def get_move(
        self, board: ConnectFourBoard, piece: PieceEnum, model_name: str
    ) -> Move | None:
        pass
