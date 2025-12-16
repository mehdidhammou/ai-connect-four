from math import inf

from src.board.connect_four_board import ConnectFourBoard
from src.heuristic import Heuristic
from src.types.move import Move

from .solver import Solver


class MinimaxAlphaBetaPruningSolver(Solver):
    def __init__(self, heuristic: Heuristic, depth: int):
        self.depth = depth
        self.heuristic = heuristic

    def solve(self, board: ConnectFourBoard) -> Move | None:
        _, move = self.minimax_alpha_beta_pruning(
            board=board,
            depth=self.depth,
            alpha=-inf,
            beta=inf,
            max_player=True,
        )
        return move

    def minimax_alpha_beta_pruning(
        self,
        board: ConnectFourBoard,
        depth,
        alpha,
        beta,
        max_player,
    ) -> tuple[float, Move | None]:
        if depth == 0 or not board.get_possible_moves():
            return self.heuristic.evaluate(board=board, piece=2), None

        possible_moves = board.get_possible_moves()
        if max_player:
            max_eval = -inf
            best_move: Move | None = None

            for move in possible_moves:
                new_board = ConnectFourBoard(initial_state=board.state)

                new_board.make_move(move=move, piece=2)

                eval, _ = self.minimax_alpha_beta_pruning(
                    board=new_board,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    max_player=False,
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

                new_board.make_move(move=move, piece=1)

                eval, _ = self.minimax_alpha_beta_pruning(
                    board=new_board,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    max_player=True,
                )

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)

                if beta <= alpha:
                    break

            return min_eval, best_move
