import unittest
from src.types.piece_enum import PieceEnum
from src.heuristic import CountPiecesHeuristic
from src.board import ConnectFourBoard


class TestCountPiecesHeuristic(unittest.TestCase):
    def test_evaluate(self):
        board = ConnectFourBoard()
        heuristic = CountPiecesHeuristic()

        # Test when player 1 has won
        board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0],
        ]
        self.assertEqual(heuristic.evaluate(board, PieceEnum.HUMAN), 999_999)

        # Test when player 2 has won
        board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 0, 0, 0],
        ]
        self.assertEqual(-heuristic.evaluate(board, PieceEnum.CPU), -999_999)

        # Test when there is no win
        board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 2, 1, 2, 1, 2, 1],
        ]
        self.assertEqual(heuristic.evaluate(board, PieceEnum.HUMAN), 0)

    def test_evaluate_board(self):
        board = ConnectFourBoard()
        heuristic = CountPiecesHeuristic()

        # Test when there are consecutive pieces in rows
        board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0],
        ]
        self.assertEqual(heuristic._evaluate_board(board, PieceEnum.HUMAN), 15)

        # Test when there are consecutive pieces in columns
        board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0, 0],
        ]
        self.assertEqual(heuristic._evaluate_board(board, PieceEnum.HUMAN), 30)

        # Test when there are consecutive pieces in diagonals
        board.state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
        ]
        self.assertEqual(heuristic._evaluate_board(board, PieceEnum.HUMAN), 15)

    def test_evaluateWindow(self):
        heuristic = CountPiecesHeuristic()

        # Test when there are 3 consecutive pieces and 1 empty space
        window = [1, 1, 1, 0]
        self.assertEqual(heuristic.evaluateWindow(window, PieceEnum.HUMAN), 10)

        # Test when there are 2 consecutive pieces and 2 empty spaces
        window = [1, 1, 0, 0]
        self.assertEqual(heuristic.evaluateWindow(window, PieceEnum.HUMAN), 5)
        # Test when there are no consecutive pieces
        window = [1, 0, 2, 0]
        self.assertEqual(heuristic.evaluateWindow(window, PieceEnum.HUMAN), 0)


if __name__ == "__main__":
    unittest.main()
