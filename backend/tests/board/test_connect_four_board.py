from unittest import TestCase
from src.board.connect_four_board import ConnectFourBoard
from random import random


class TestConnectFourBoard(TestCase):
    def setUp(self):
        self.board = ConnectFourBoard()

    def test_board_init(self):
        self.assertEqual(self.board.cols, 7)
        self.assertEqual(self.board.rows, 6)
        self.assertEqual(self.board.state, [[0] * 7 for _ in range(6)])

    def test_board_init_with_params(self):
        initial_state = [[int(random() * 3) for _ in range(7)] for _ in range(6)]
        board = ConnectFourBoard(initial_state)
        self.assertEqual(board.state, initial_state)

    def test_board_init_with_invalid_params(self):
        initial_state = [[int(random() * 3) for _ in range(10)] for _ in range(10)]
        with self.assertRaises(ValueError):
            ConnectFourBoard(initial_state)

    def test_get_possible_moves(self):
        board = ConnectFourBoard()
        expected_moves = [
            {"col": 0, "row": 5},
            {"col": 1, "row": 5},
            {"col": 2, "row": 5},
            {"col": 3, "row": 5},
            {"col": 4, "row": 5},
            {"col": 5, "row": 5},
            {"col": 6, "row": 5},
        ]
        self.assertEqual(board.get_possible_moves(), expected_moves)

        # Test when the board has some pieces already placed
        initial_state = [[0] * 7 for _ in range(5)]
        initial_state.append([1, 2, 1, 2, 1, 2, 1])
        board = ConnectFourBoard(initial_state)
        expected_moves = [
            {"col": 0, "row": 4},
            {"col": 1, "row": 4},
            {"col": 2, "row": 4},
            {"col": 3, "row": 4},
            {"col": 4, "row": 4},
            {"col": 5, "row": 4},
            {"col": 6, "row": 4},
        ]
        self.assertEqual(board.get_possible_moves(), expected_moves)

    def test_has_won_horizontal(self):
        # Test when there is a horizontal win
        initial_state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0],
        ]
        board = ConnectFourBoard(initial_state)
        self.assertTrue(board.has_won(1))
        self.assertEqual(
            board.winning_sequence,
            [
                {"row": 5, "col": 0},
                {"row": 5, "col": 1},
                {"row": 5, "col": 2},
                {"row": 5, "col": 3},
            ],
        )

    def test_has_won_vertical(self):
        # Test when there is a vertical win
        initial_state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0, 0],
        ]
        board = ConnectFourBoard(initial_state)
        self.assertTrue(board.has_won(1))
        self.assertEqual(
            board.winning_sequence,
            [
                {"row": 2, "col": 0},
                {"row": 3, "col": 0},
                {"row": 4, "col": 0},
                {"row": 5, "col": 0},
            ],
        )

    def test_has_won_diagonal(self):
        # Test when there is a diagonal win
        initial_state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
        ]
        board = ConnectFourBoard(initial_state)
        self.assertTrue(board.has_won(1))
        self.assertCountEqual(
            board.winning_sequence,
            [
                {"row": 5, "col": 0},
                {"row": 4, "col": 1},
                {"row": 3, "col": 2},
                {"row": 2, "col": 3},
            ],
        )

    def test_has_won_no_win(self):
        # Test when there is no win
        initial_state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 2, 1, 2, 1, 2, 1],
        ]
        board = ConnectFourBoard(initial_state)
        self.assertFalse(board.has_won(1))
        self.assertEqual(board.winning_sequence, [])
