from typing import Type
from src.game import GameState
from src.types.move import Move


class Response:
    def __init__(
        self,
        message: str,
        state: GameState,
        board: list[list[int]],
        sequence: list[Move] | None,
    ):
        self.message = message
        self.board = board
        self.state = state
        self.sequence = sequence

    def __repr__(self):
        return f"Response(message={self.message}, board={self.board}, sequence={self.sequence}, state={self.state})"

    def __str__(self):
        return f"Response(message={self.message}, board={self.board}, sequence={self.sequence}, state={self.state})"
