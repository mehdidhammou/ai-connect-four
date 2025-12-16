from unittest import TestCase

from api.schemas.move import Move
from src.board.connect_four_board import ConnectFourBoard
from src.game import Game, GameState
from src.solver import Solver


class MockSolver(Solver):
    def solve(self, board: ConnectFourBoard) -> Move:
        possible_moves = board.get_possible_moves()
        return possible_moves[0]  # Always return the first column as the best move


class TestGame(TestCase):
    def setUp(self):
        self.board = ConnectFourBoard()
        self.solver = MockSolver()
        self.game = Game(self.board, self.solver)

    def test_play(self):
        self.game.play(1)
        self.assertEqual(self.board.state[5][0], 1)

    def test_sync_state_win(self):
        self.board.state = [
            [1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
        self.game.sync_state()
        self.assertEqual(self.game.state, GameState.WIN)

    def test_sync_state_lose(self):
        self.board.state = [
            [2, 2, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
        self.game.sync_state()
        self.assertEqual(self.game.state, GameState.LOSE)

    def test_sync_state_tie(self):
        self.board.state = [
            [1, 2, 1, 2, 1, 2, 1],
            [2, 2, 2, 1, 2, 1, 2],
            [1, 1, 1, 2, 2, 2, 1],
            [2, 2, 1, 2, 1, 1, 1],
            [1, 2, 1, 1, 1, 2, 1],
            [2, 1, 2, 2, 2, 1, 2],
        ]
        self.game.sync_state()
        self.assertEqual(self.game.state, GameState.TIE)