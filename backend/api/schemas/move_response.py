from pydantic import BaseModel
from src.game.game_state import GameState
from src.types.move import Move


class MoveResponse(BaseModel):
    state: GameState
    solver_move: Move | None
    winning_sequence: list[Move] | None
