from src.board.connect_four_board import ConnectFourBoard
from src.types.move import Move

from .heuristic import Heuristic


class CountPositionsHeuristic(Heuristic):
    def __init__(self, id: int) -> None:
        super().__init__(id=id)

    @staticmethod
    def evaluate(board: ConnectFourBoard, piece: int) -> float:
        if board.has_won(1):
            return 100_000

        if board.has_won(2):
            return -100_000

        score = 0
        score += 4 * CountPositionsHeuristic._evaluate_center_control(board, piece)
        score += 1 * CountPositionsHeuristic._evaluate_corner_control(
            board, piece
        )  # Give corners higher weight
        score += 0.5 * CountPositionsHeuristic._evaluate_side_control(
            board, piece
        )  # Give sides lower weight
        score += CountPositionsHeuristic._check_double_sided_win(board, piece)
        score += 20 * CountPositionsHeuristic._check_blocking_move(board, piece)
        score += 1000 * CountPositionsHeuristic._check_winning_move(board, piece)

        return score

    @staticmethod
    def first_play() -> Move:
        return {"col": 3, "row": 0}

    @staticmethod
    def _evaluate_center_control(board: ConnectFourBoard, piece: int):
        center_col = board.cols // 2
        center_count = 0

        for row in range(board.rows):
            if board.state[row][center_col] == piece:
                center_count += 1

        return center_count

    @staticmethod
    def _evaluate_corner_control(board: ConnectFourBoard, piece: int):
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
    def _evaluate_side_control(board: ConnectFourBoard, piece: int):
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
    def _check_double_sided_win(board: ConnectFourBoard, piece: int):
        opponent_piece = 3 - piece

        # Check for potential double-sided wins in rows
        for row in range(board.rows):
            for col in range(board.cols - 3):
                window = [board.state[row][col + i] for i in range(4)]
                if (
                    window[1] == opponent_piece
                    and window[2] == opponent_piece
                    and window.count(0) == 2
                ):
                    return -1000  # Penalize the opponent for potential double-sided win

        # Check for potential double-sided wins in diagonals (bottom-left to top-right)
        for row in range(3, board.rows):
            for col in range(board.cols - 3):
                window = [board.state[row - i][col + i] for i in range(4)]
                if (
                    window[1] == opponent_piece
                    and window[2] == opponent_piece
                    and window.count(0) == 2
                ):
                    return -1000

        # Check for potential double-sided wins in diagonals (top-left to bottom-right)
        for row in range(board.rows - 3):
            for col in range(board.cols - 3):
                window = [board.state[row + i][col + i] for i in range(4)]
                if (
                    window[1] == opponent_piece
                    and window[2] == opponent_piece
                    and window.count(0) == 2
                ):
                    return -1000

        return 0

    @staticmethod
    def _check_blocking_move(board: ConnectFourBoard, piece: int):
        # Check for potential blocking moves in rows
        for row in range(board.rows):
            for col in range(board.cols - 3):
                window = [board.state[row][col + i] for i in range(4)]
                if window.count(piece) == 3 and window.count(0) == 1:
                    return 50  # Encourage blocking opponent's winning move

        # Check for potential blocking moves in diagonals (bottom-left to top-right)
        for row in range(3, board.rows):
            for col in range(board.cols - 3):
                window = [board.state[row - i][col + i] for i in range(4)]
                if window.count(piece) == 3 and window.count(0) == 1:
                    return 50

        # Check for potential blocking moves in diagonals (top-left to bottom-right)
        for row in range(board.rows - 3):
            for col in range(board.cols - 3):
                window = [board.state[row + i][col + i] for i in range(4)]
                if window.count(piece) == 3 and window.count(0) == 1:
                    return 50

        # Check for potential blocking moves in columns
        for col in range(board.cols):
            for row in range(board.rows - 3):
                window = [board.state[row + i][col] for i in range(4)]
                if window.count(piece) == 3 and window.count(0) == 1:
                    return 50

        return 0

    @staticmethod
    def _check_winning_move(board: ConnectFourBoard, piece: int):
        # Check for potential winning moves in rows
        for row in range(board.rows):
            for col in range(board.cols - 3):
                window = [board.state[row][col + i] for i in range(4)]
                if window.count(piece) == 3 and window.count(0) == 1:
                    return 100  # Encourage making winning move

        # Check for potential winning moves in diagonals (bottom-left to top-right)
        for row in range(3, board.rows):
            for col in range(board.cols - 3):
                window = [board.state[row - i][col + i] for i in range(4)]
                if window.count(piece) == 3 and window.count(0) == 1:
                    return 100

        # Check for potential winning moves in diagonals (top-left to bottom-right)
        for row in range(board.rows - 3):
            for col in range(board.cols - 3):
                window = [board.state[row + i][col + i] for i in range(4)]
                if window.count(piece) == 3 and window.count(0) == 1:
                    return 100

        # Check for potential winning moves in columns
        for col in range(board.cols):
            for row in range(board.rows - 3):
                window = [board.state[row + i][col] for i in range(4)]
                if window.count(piece) == 3 and window.count(0) == 1:
                    return 100

        return 0
