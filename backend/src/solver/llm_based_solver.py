from src.types.piece import Piece
from .solver import Solver
from src.model import ModelProvider
from src.board.connect_four_board import ConnectFourBoard
from src.types.move import Move


class LLMBasedSolver(Solver):
    def __init__(self, model_provider: ModelProvider, model_name: str) -> None:
        self.model_provider = model_provider
        self.model_name = model_name

    def solve(self, board: ConnectFourBoard, piece: Piece) -> Move | None:
        return self.model_provider.get_move(
            board=board, piece=piece, model_name=self.model_name
        )
