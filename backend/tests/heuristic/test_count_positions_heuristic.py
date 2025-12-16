import unittest

from src.board import ConnectFourBoard
from src.heuristic import (
    CountPositionsHeuristic,
)


class TestCountPositionsHeuristic(unittest.TestCase):
    def setUp(self):
        self.heuristic = CountPositionsHeuristic(id=1)
        self.board = ConnectFourBoard()

    def test_evaluate_center_control(self):
        self.board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
        ]
        self.assertEqual(self.heuristic.evaluate_center_control(self.board, 1), 4)

    def test_evaluate_corner_control(self):
        self.board.state = [
            [1, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 1],
        ]
        self.assertEqual(self.heuristic.evaluate_corner_control(self.board, 1), 4)

    def test_evaluate_side_control(self):
        self.board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0],
        ]
        self.assertEqual(self.heuristic.evaluate_side_control(self.board, 1), 4)

    def test_check_double_sided_win(self):
        self.board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
        self.assertEqual(self.heuristic.check_double_sided_win(self.board, 1), -1000)

    def test_check_blocking_move(self):
        self.board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0],
        ]
        self.assertEqual(self.heuristic.check_blocking_move(self.board, 1), 50)

    def test_check_winning_move(self):
        self.board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0],
        ]
        self.assertEqual(self.heuristic.check_winning_move(self.board, 1), 100)

    def test_evaluate(self):
        self.board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0],
        ]
        101002.5
        self.assertEqual(self.heuristic.evaluate(self.board, 1), 101002.5)
