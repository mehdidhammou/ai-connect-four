from .move import Move
from src.game import GameState


class Response:
    def __init__(
        self,
        message: str,
        state: GameState,
        board: list[list[int]],
        sequence: list[Move] = None,
        success: bool = True,
    ):
        self.message = message
        self.board = board
        self.state = state
        self.sequence = sequence
        self.success = success

    def __repr__(self):
        return f"Response(message={self.message}, board={self.board}, sequence={self.sequence}, success={self.success}, state={self.state})"

    def __str__(self):
        return f"Response(message={self.message}, board={self.board}, sequence={self.sequence}, success={self.success} state={self.state})"
