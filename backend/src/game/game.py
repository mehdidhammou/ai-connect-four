from src.types.piece import Piece
from src.types.move import Move
from src.board.connect_four_board import ConnectFourBoard
from src.solver import Solver
from .game_state import GameState


class Game:
    def __init__(
        self,
        board: ConnectFourBoard,
        solver: Solver,
        auto: bool = False,
    ):
        self.board = board
        self.solver = solver
        self.state = GameState.CONTINUE
        self.auto = auto
        self.sync_state()

    def make_move(self, move: Move, piece: Piece):
        if move not in self.board.get_possible_moves():
            raise ValueError("Invalid move")
        self.board.make_move(move=move, piece=piece)
        self.sync_state()

    def get_solver_move(self, piece: Piece) -> Move | None:
        return self.solver.solve(self.board, piece=piece)

    def sync_state(self) -> None:
        if self.board.has_won(1):
            self.state = GameState.MM_POS_WIN if self.auto else GameState.WIN
        elif self.board.has_won(2):
            self.state = GameState.MM_PIECE_WIN if self.auto else GameState.LOSE
        elif not self.board.get_possible_moves():
            self.state = GameState.TIE

    def get_winning_sequence(self):
        return self.board.winning_sequence

    def is_over(self) -> bool:
        return self.state != GameState.CONTINUE
