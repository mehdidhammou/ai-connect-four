from unittest import TestCase

from src.board.connect_four_board import ConnectFourBoard
from src.solver import Solver
from src.types.move import Move
from src.types.piece_enum import PieceEnum
from src.game.game import Game


class MockSolver(Solver):
    def solve(self, board: ConnectFourBoard, piece: PieceEnum) -> Move:
        possible_moves = board.get_possible_moves()
        return possible_moves[0]  # Always return the first column as the best move

    def first_move(self) -> Move:
        possible_moves = ConnectFourBoard().get_possible_moves()
        return possible_moves[0]


class TestGame(TestCase):
    def setUp(self):
        self.board = ConnectFourBoard()
        self.solver = MockSolver()
        self.game = Game(self.board, self.solver)

    def test_play(self):
        move = self.game.get_solver_move(piece=PieceEnum.CPU)
        self.assertEqual(move, Move(col=0, row=5))

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
        self.assertEqual(self.game.state, "WIN")

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
        self.assertEqual(self.game.state, "LOSE")

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
        self.assertEqual(self.game.state, "TIE")
