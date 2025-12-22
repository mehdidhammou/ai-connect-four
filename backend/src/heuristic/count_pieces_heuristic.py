from .heuristic import Heuristic
from src.board.connect_four_board import ConnectFourBoard
from src.types.move import Move


class CountPiecesHeuristic(Heuristic):
    def __init__(self, id: int) -> None:
        super().__init__(id=id)

    @staticmethod
    def evaluate(board: ConnectFourBoard, piece) -> int:
        if board.has_won(piece=piece):
            return 999_999

        return CountPiecesHeuristic._evaluate_board(board, piece)

    @staticmethod
    def first_play() -> Move:
        return Move(col=0, row=0)

    @staticmethod
    def _evaluate_board(board: ConnectFourBoard, piece):
        score = 0
        # Evaluate based on consecutive pieces in rows
        for row in range(board.rows):
            for col in range(board.cols - 3):
                window = board.state[row][col : col + 4]
                score += CountPiecesHeuristic.evaluateWindow(window, piece)

        # Evaluate based on consecutive pieces in columns
        for col in range(board.cols):
            for row in range(board.rows - 3):
                window = [board.state[row + i][col] for i in range(4)]
                score += CountPiecesHeuristic.evaluateWindow(window, piece)

        # Evaluate based on consecutive pieces in diagonals (bottom-left to top-right)
        for row in range(3, board.rows):
            for col in range(board.cols - 3):
                window = [board.state[row - i][col + i] for i in range(4)]
                score += CountPiecesHeuristic.evaluateWindow(window, piece)

        # Evaluate based on consecutive pieces in diagonals (top-left to bottom-right)
        for row in range(board.rows - 3):
            for col in range(board.cols - 3):
                window = [board.state[row + i][col + i] for i in range(4)]
                score += CountPiecesHeuristic.evaluateWindow(window, piece)

        return score

    @staticmethod
    def evaluateWindow(window: list, piece):
        if window.count(piece) == 3 and window.count(0) == 1:
            return 10  # Encourage completing a winning sequence
        elif window.count(piece) == 2 and window.count(0) == 2:
            return 5  # Encourage creating opportunities
        else:
            return 0
