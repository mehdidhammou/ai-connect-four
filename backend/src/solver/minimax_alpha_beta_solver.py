from math import inf

from src.board.connect_four_board import ConnectFourBoard
from src.heuristic import Heuristic
from src.types.move import Move
from src.types.piece import Piece

from .solver import Solver


class MinimaxAlphaBetaPruningSolver(Solver):
    def __init__(self, heuristic: Heuristic, depth: int):
        self.depth = depth
        self.heuristic = heuristic

    def solve(self, board: ConnectFourBoard, piece: Piece) -> Move | None:
        _, best_move = self.minimax_alpha_beta_pruning(
            board=board,
            depth=self.depth,
            alpha=-inf,
            beta=inf,
            max_player=True,
            piece=piece,
        )
        return best_move

    def minimax_alpha_beta_pruning(
        self,
        board: ConnectFourBoard,
        depth,
        alpha,
        beta,
        max_player,
        piece: Piece,
    ) -> tuple[float, Move | None]:
        if board.has_won(piece=piece):
            return 999_999, None
        if board.has_won(piece=3 - piece):
            return -999_999, None

        if depth == 0 or not board.get_possible_moves():
            return self.heuristic.evaluate(board=board, piece=piece), None

        possible_moves = board.get_possible_moves()
        if max_player:
            max_eval = -inf
            best_move: Move | None = None

            for move in possible_moves:
                new_board = ConnectFourBoard(initial_state=board.state)

                new_board.make_move(move=move, piece=piece)

                eval, _ = self.minimax_alpha_beta_pruning(
                    board=new_board,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    max_player=False,
                    piece=piece,
                )

                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, eval)

                if beta <= alpha:
                    break

            return max_eval, best_move

        else:
            min_eval = inf
            best_move = None
            for move in possible_moves:
                new_board = ConnectFourBoard(initial_state=board.state)

                new_board.make_move(move=move, piece=3 - piece)

                eval, _ = self.minimax_alpha_beta_pruning(
                    board=new_board,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    max_player=True,
                    piece=piece,
                )

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)

                if beta <= alpha:
                    break

            return min_eval, best_move
