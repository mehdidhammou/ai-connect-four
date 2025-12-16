from src.board.connect_four_board import ConnectFourBoard
from src.solver import Solver
from .game_state import GameState


class Game:
    def __init__(
        self,
        board: ConnectFourBoard,
        solver: Solver,
        cpu_vs_cpu: bool = False,
    ):
        self.board = board
        self.solver = solver
        self.state = GameState.CONTINUE
        self.cpu_vs_cpu = cpu_vs_cpu
        self.sync_state()

    def play(self, piece: int) -> None:
        best_move = self.solver.solve(self.board)
        self.board.make_move(move=best_move, piece=piece)
        self.sync_state()

    def sync_state(self) -> None:
        if self.board.has_won(1):
            self.state = GameState.MM_PIECE_WIN if self.cpu_vs_cpu else GameState.WIN
        elif self.board.has_won(2):
            self.state = GameState.MM_POS_WIN if self.cpu_vs_cpu else GameState.LOSE
        elif not self.board.get_possible_moves():
            self.state = GameState.TIE

    def reset(self):
        self.board.state = [
            [0 for _ in range(self.board.cols)] for _ in range(self.board.rows)
        ]

    def is_over(self):
        return self.state != GameState.CONTINUE

    def is_a_tie(self):
        return self.state == GameState.TIE
