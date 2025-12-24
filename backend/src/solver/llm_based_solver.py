from src.types.piece_enum import PieceEnum
from .solver import Solver
from src.model import ModelProvider
from src.board.connect_four_board import ConnectFourBoard
from src.types.move import Move


class LLMBasedSolver(Solver):
    def __init__(self, model_provider: ModelProvider, model_name: str) -> None:
        self.model_provider = model_provider
        self.model_name = model_name

    def solve(self, board: ConnectFourBoard, piece: PieceEnum) -> Move | None:
        if piece not in [PieceEnum.HUMAN, PieceEnum.CPU]:
            raise ValueError("Invalid piece for LLMBasedSolver.")

        return self.model_provider.get_move(
            board=board,
            piece=piece,
            model_name=self.model_name,
        )

    def first_move(self) -> Move:
        return self.model_provider.get_first_move(model_name=self.model_name)
