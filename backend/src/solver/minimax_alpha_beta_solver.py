from math import inf

from src.board.connect_four_board import ConnectFourBoard
from src.heuristic import Heuristic
from src.types.move import Move
from src.types.piece_enum import PieceEnum

from .solver import Solver


class MinimaxAlphaBetaPruningSolver(Solver):
    def __init__(self, heuristic: Heuristic, depth: int):
        self.depth = depth
        self.heuristic = heuristic

    def solve(self, board: ConnectFourBoard, piece: PieceEnum) -> Move | None:
        if piece not in [PieceEnum.HUMAN, PieceEnum.CPU]:
            raise ValueError("Invalid piece for MinimaxAlphaBetaPruningSolver.")

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
        piece: PieceEnum,
    ) -> tuple[float, Move | None]:
        if depth == 0 or not board.get_possible_moves():
            sign = 1 if max_player else -1
            return sign * self.heuristic.evaluate(board=board, piece=piece), None

        possible_moves = board.get_possible_moves()
        if max_player:
            max_eval = -inf
            best_move: Move | None = None

            for move in possible_moves:
                new_board = ConnectFourBoard(initial_state=board.state)

                new_board.make_move(move=move, piece=piece)

                if new_board.has_won(piece=piece):
                    return 999_999, move

                eval, _ = self.minimax_alpha_beta_pruning(
                    board=new_board,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    max_player=False,
                    piece=PieceEnum(3 - piece.value),
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

                new_board.make_move(move=move, piece=piece)

                if new_board.has_won(piece=piece):
                    return -999_999, move

                eval, _ = self.minimax_alpha_beta_pruning(
                    board=new_board,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    max_player=True,
                    piece=PieceEnum(3 - piece.value),
                )

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)

                if beta <= alpha:
                    break

            return min_eval, best_move
