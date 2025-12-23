from src.board.connect_four_board import ConnectFourBoard
from src.types.move import Move
from src.types.piece_enum import PieceEnum

from .heuristic import Heuristic


class CountPositionsHeuristic(Heuristic):
    @staticmethod
    def evaluate(board: ConnectFourBoard, piece: PieceEnum) -> float:
        if board.has_won(piece=piece):
            return 999_999

        score = 0
        score += 4 * CountPositionsHeuristic._evaluate_center_control(board, piece)
        score += 1 * CountPositionsHeuristic._evaluate_corner_control(board, piece)
        score += 0.5 * CountPositionsHeuristic._evaluate_side_control(board, piece)
        score += CountPositionsHeuristic._check_double_sided_win(board, piece)
        score += 20 * CountPositionsHeuristic._check_blocking_move(board, piece)
        score += 1000 * CountPositionsHeuristic._check_winning_move(board, piece)

        return score

    @staticmethod
    def first_play() -> Move:
        return Move(col=3, row=0)

    @staticmethod
    def _evaluate_center_control(board: ConnectFourBoard, piece: PieceEnum):
        center_col = board.cols // 2
        center_count = 0

        for row in range(board.rows):
            if board.state[row][center_col] == piece:
                center_count += 1

        return center_count

    @staticmethod
    def _evaluate_corner_control(board: ConnectFourBoard, piece: PieceEnum):
        corner_count = 0

        if board.state[0][0] == piece:
            corner_count += 1
        if board.state[0][board.cols - 1] == piece:
            corner_count += 1
        if board.state[board.rows - 1][0] == piece:
            corner_count += 1
        if board.state[board.rows - 1][board.cols - 1] == piece:
            corner_count += 1

        return corner_count

    @staticmethod
    def _evaluate_side_control(board: ConnectFourBoard, piece: PieceEnum):
        side_count = 0

        for row in range(board.rows):
            if board.state[row][0] == piece:
                side_count += 1
            if board.state[row][board.cols - 1] == piece:
                side_count += 1

        for col in range(1, board.cols - 1):
            if board.state[0][col] == piece:
                side_count += 1
            if board.state[board.rows - 1][col] == piece:
                side_count += 1

        return side_count

    @staticmethod
    def _check_double_sided_win(board: ConnectFourBoard, piece: PieceEnum):
        opponent_piece = PieceEnum(3 - piece.value)

        # Check for potential double-sided wins in rows
        for row in range(board.rows):
            for col in range(board.cols - 3):
                window = [board.state[row][col + i] for i in range(4)]
                if (
                    window[1] == opponent_piece
                    and window[2] == opponent_piece
                    and window.count(PieceEnum.EMPTY) == 2
                ):
                    return -1000  # Penalize the opponent for potential double-sided win

        # Check for potential double-sided wins in diagonals (bottom-left to top-right)
        for row in range(3, board.rows):
            for col in range(board.cols - 3):
                window = [board.state[row - i][col + i] for i in range(4)]
                if (
                    window[1] == opponent_piece
                    and window[2] == opponent_piece
                    and window.count(PieceEnum.EMPTY) == 2
                ):
                    return -1000

        # Check for potential double-sided wins in diagonals (top-left to bottom-right)
        for row in range(board.rows - 3):
            for col in range(board.cols - 3):
                window = [board.state[row + i][col + i] for i in range(4)]
                if (
                    window[1] == opponent_piece
                    and window[2] == opponent_piece
                    and window.count(PieceEnum.EMPTY) == 2
                ):
                    return -1000

        return 0

    @staticmethod
    def _check_blocking_move(board: ConnectFourBoard, piece: PieceEnum):
        # Check for potential blocking moves in rows
        for row in range(board.rows):
            for col in range(board.cols - 3):
                window = [board.state[row][col + i] for i in range(4)]
                if window.count(piece) == 3 and window.count(PieceEnum.EMPTY) == 1:
                    return 50  # Encourage blocking opponent's winning move

        # Check for potential blocking moves in diagonals (bottom-left to top-right)
        for row in range(3, board.rows):
            for col in range(board.cols - 3):
                window = [board.state[row - i][col + i] for i in range(4)]
                if window.count(piece) == 3 and window.count(PieceEnum.EMPTY) == 1:
                    return 50

        # Check for potential blocking moves in diagonals (top-left to bottom-right)
        for row in range(board.rows - 3):
            for col in range(board.cols - 3):
                window = [board.state[row + i][col + i] for i in range(4)]
                if window.count(piece) == 3 and window.count(PieceEnum.EMPTY) == 1:
                    return 50

        # Check for potential blocking moves in columns
        for col in range(board.cols):
            for row in range(board.rows - 3):
                window = [board.state[row + i][col] for i in range(4)]
                if window.count(piece) == 3 and window.count(PieceEnum.EMPTY) == 1:
                    return 50

        return 0

    @staticmethod
    def _check_winning_move(board: ConnectFourBoard, piece: PieceEnum):
        # Check for potential winning moves in rows
        for row in range(board.rows):
            for col in range(board.cols - 3):
                window = [board.state[row][col + i] for i in range(4)]
                if window.count(piece) == 3 and window.count(PieceEnum.EMPTY) == 1:
                    return 100  # Encourage making winning move

        # Check for potential winning moves in diagonals (bottom-left to top-right)
        for row in range(3, board.rows):
            for col in range(board.cols - 3):
                window = [board.state[row - i][col + i] for i in range(4)]
                if window.count(piece) == 3 and window.count(PieceEnum.EMPTY) == 1:
                    return 100

        # Check for potential winning moves in diagonals (top-left to bottom-right)
        for row in range(board.rows - 3):
            for col in range(board.cols - 3):
                window = [board.state[row + i][col + i] for i in range(4)]
                if window.count(piece) == 3 and window.count(PieceEnum.EMPTY) == 1:
                    return 100

        # Check for potential winning moves in columns
        for col in range(board.cols):
            for row in range(board.rows - 3):
                window = [board.state[row + i][col] for i in range(4)]
                if window.count(piece) == 3 and window.count(PieceEnum.EMPTY) == 1:
                    return 100

        return 0
