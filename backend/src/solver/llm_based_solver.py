from src.board.connect_four_board import ConnectFourBoard
from src.model import ModelProvider
from src.types.model import Model
from src.types.move import Move
from src.types.piece_enum import PieceEnum

from .solver import Solver


class LLMBasedSolver(Solver):
    def __init__(self, model_provider: ModelProvider, model: Model) -> None:
        self.model_provider = model_provider
        self.model = model

    def solve(self, board: ConnectFourBoard, piece: PieceEnum) -> Move | None:
        if piece not in [PieceEnum.HUMAN, PieceEnum.CPU]:
            raise ValueError("Invalid piece for LLMBasedSolver.")

        return self.model_provider.get_move(
            board=board,
            piece=piece,
            model_name=self.model.name,
        )

    def first_move(self) -> Move:
        return self.model_provider.get_first_move(model_name=self.model.name)
