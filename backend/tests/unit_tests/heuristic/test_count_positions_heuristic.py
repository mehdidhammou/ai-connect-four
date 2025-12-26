import unittest

from src.board import ConnectFourBoard
from src.heuristic.count_positions_heuristic import CountPositionsHeuristic
from src.types.piece_enum import PieceEnum


class TestCountPositionsHeuristic(unittest.TestCase):
    def setUp(self):
        self.heuristic = CountPositionsHeuristic()
        self.board = ConnectFourBoard()

    def test_evaluate_center_control(self):
        self.board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0],
        ]
        self.assertEqual(
            self.heuristic._evaluate_center_control(self.board, PieceEnum.CPU), 4
        )

    def test_evaluate_corner_control(self):
        self.board.state = [
            [2, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 2],
        ]
        self.assertEqual(
            self.heuristic._evaluate_corner_control(self.board, PieceEnum.CPU), 4
        )

    def test_evaluate_side_control(self):
        self.board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0],
        ]
        self.assertEqual(
            self.heuristic._evaluate_side_control(self.board, PieceEnum.CPU), 4
        )

    def test_check_double_sided_win(self):
        self.board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
        self.assertEqual(
            self.heuristic._check_double_sided_win(self.board, PieceEnum.CPU), -1000
        )

    def test_check_blocking_move(self):
        self.board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 0, 0, 0, 0],
        ]
        self.assertEqual(
            self.heuristic._check_blocking_move(self.board, PieceEnum.CPU), 50
        )

    def test_check_winning_move(self):
        self.board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 0, 0, 0, 0],
        ]
        self.assertEqual(
            self.heuristic._check_winning_move(self.board, PieceEnum.CPU), 100
        )

    def test_evaluate(self):
        self.board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 0, 0, 0, 0],
        ]
        self.assertEqual(self.heuristic.evaluate(self.board, PieceEnum.CPU), 101002.5)
