from backend.api.schemas.move import Move
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

    def play(self, piece: int) -> Move | None:
        best_move = self.solver.solve(self.board)
        self.board.make_move(move=best_move, piece=piece)
        self.sync_state()
        return best_move

    def sync_state(self) -> None:
        if self.board.has_won(1):
            self.state = GameState.OVER if self.cpu_vs_cpu else GameState.WIN
        elif self.board.has_won(2):
            self.state = GameState.OVER if self.cpu_vs_cpu else GameState.LOSE
        elif not self.board.get_possible_moves():
            self.state = GameState.TIE

    def get_winning_sequence(self):
        return self.board.winning_sequence
