from src.board.connect_four_board import ConnectFourBoard
from src.solver import Solver
from src.types.move import Move
from src.types.piece_enum import PieceEnum

from .game_state import GameState


class Game:
    def __init__(
        self,
        board: ConnectFourBoard,
        solver: Solver,
    ):
        self.board = board
        self.solver = solver
        self.state: GameState = "CONTINUE"
        self.sync_state()

    def make_move(self, move: Move, piece: PieceEnum) -> None:
        if move not in self.board.get_possible_moves():
            raise ValueError("Invalid move")
        self.board.make_move(move=move, piece=piece)
        self.sync_state()

    def get_solver_move(self, piece: PieceEnum) -> Move | None:
        return self.solver.solve(self.board, piece=piece)

    def sync_state(self) -> None:
        if self.board.has_won(piece=PieceEnum.HUMAN):
            self.state = "WIN"
        elif self.board.has_won(piece=PieceEnum.CPU):
            self.state = "LOSE"
        elif not self.board.get_possible_moves():
            self.state = "TIE"

    def get_winning_sequence(self):
        return self.board.winning_sequence

    def is_over(self) -> bool:
        return self.state != "CONTINUE"
