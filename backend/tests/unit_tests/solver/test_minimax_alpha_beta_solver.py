import unittest

from src.types.piece_enum import PieceEnum
from src.board.connect_four_board import ConnectFourBoard
from src.heuristic import CountPositionsHeuristic
from src.solver import MinimaxAlphaBetaPruningSolver
from src.types.move import Move


class TestMinimaxAlphaBetaSolverComprehensive(unittest.TestCase):
    def setUp(self):
        self.heuristic = CountPositionsHeuristic()
        self.solver = MinimaxAlphaBetaPruningSolver(heuristic=self.heuristic, depth=2)
        self.board = ConnectFourBoard()

    def test_max_player_winning_move(self):
        self.board.state = [[0] * 7 for _ in range(5)] + [[2, 2, 2, 0, 1, 1, 0]]
        move = self.solver.solve(board=self.board, piece=PieceEnum.CPU)
        expected_move = Move(col=3, row=5)
        self.assertEqual(move, expected_move)

    def test_min_player_blocking_move(self):
        self.board.state = [[0] * 7 for _ in range(5)] + [[2, 2, 2, 0, 1, 1, 0]]
        move = self.solver.solve(board=self.board, piece=PieceEnum.CPU)
        expected_move = Move(col=3, row=5)
        self.assertEqual(move, expected_move)

    def test_heuristic_positive_for_current_player(self):
        self.board.state = [[0] * 7 for _ in range(5)] + [[2, 0, 0, 0, 0, 0, 0]]
        score = self.heuristic.evaluate(self.board, piece=PieceEnum.CPU)
        self.assertGreater(score, 0)

    def test_heuristic_win_returns_high_value(self):
        self.board.state = [[0] * 7 for _ in range(5)] + [[2, 2, 2, 2, 0, 0, 0]]
        score = self.heuristic.evaluate(self.board, piece=PieceEnum.CPU)
        self.assertEqual(score, 999_999)

    def test_solver_returns_none_on_full_board_draw(self):
        self.board.state = [
            [2, 1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2, 1],
        ]
        move = self.solver.solve(board=self.board, piece=PieceEnum.CPU)
        self.assertIsNone(move)

    def test_solver_avoids_losing_immediate(self):
        # Player 2 is about to win next turn at column 2
        self.board.state = [[0] * 7 for _ in range(5)] + [[1, 1, 1, 0, 2, 0, 0]]
        move = self.solver.solve(board=self.board, piece=PieceEnum.CPU)
        # Max player should block at column 3
        expected_move = Move(col=3, row=5)
        self.assertEqual(move, expected_move)
