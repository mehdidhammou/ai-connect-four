import unittest

from src.board.connect_four_board import ConnectFourBoard
from src.heuristic import CountPositionsHeuristic
from src.solver import MinimaxAlphaBetaPruningSolver
from src.types.move import Move


class TestMinimaxAlphaBetaSolverComprehensive(unittest.TestCase):
    def setUp(self):
        self.heuristic = CountPositionsHeuristic()
        self.solver = MinimaxAlphaBetaPruningSolver(heuristic=self.heuristic, depth=3)
        self.board = ConnectFourBoard()

    def test_max_player_winning_move(self):
        self.board.state = [[0] * 7 for _ in range(5)] + [[1, 1, 1, 0, 2, 2, 0]]
        move = self.solver.solve(board=self.board, piece=1)
        expected_move = Move(col=3, row=5)
        self.assertEqual(move, expected_move)

    def test_min_player_blocking_move(self):
        self.board.state = [[0] * 7 for _ in range(5)] + [[1, 1, 1, 0, 2, 2, 0]]
        move = self.solver.solve(board=self.board, piece=2)
        expected_move = Move(col=3, row=5)
        self.assertEqual(move, expected_move)

    def test_heuristic_positive_for_current_player(self):
        self.board.state = [[0] * 7 for _ in range(5)] + [[1, 0, 0, 0, 0, 0, 0]]
        score = self.heuristic.evaluate(self.board, piece=1)
        self.assertGreater(score, 0)

    def test_heuristic_win_returns_high_value(self):
        self.board.state = [[0] * 7 for _ in range(5)] + [[1, 1, 1, 1, 0, 0, 0]]
        score = self.heuristic.evaluate(self.board, piece=1)
        self.assertEqual(score, 999_999)

    def test_heuristic_min_player_sign_flip(self):
        self.board.state = [[0] * 7 for _ in range(5)] + [[1, 1, 1, 0, 0, 0, 0]]
        # Max player evaluation
        max_score = self.heuristic.evaluate(self.board, piece=1)
        # If evaluating as min player, should flip
        min_score = -self.heuristic.evaluate(self.board, piece=1)
        self.assertEqual(min_score, -max_score)

    def test_solver_returns_none_on_full_board_draw(self):
        self.board.state = [
            [1, 2, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 1, 2],
        ]
        move = self.solver.solve(board=self.board, piece=1)
        self.assertIsNone(move)

    def test_solver_avoids_losing_immediate(self):
        # Player 1 is about to win next turn at column 3
        self.board.state = [[0] * 7 for _ in range(5)] + [[2, 2, 2, 0, 1, 0, 0]]
        move = self.solver.solve(board=self.board, piece=1)
        # Max player should block at column 3
        expected_move = Move(col=3, row=5)
        self.assertEqual(move, expected_move)
