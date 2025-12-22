from pydantic import BaseModel
from src.game.game_state import GameState
from src.types.move import Move


class MoveResponse(BaseModel):
    state: GameState
    move: Move | None
    sequence: list[Move] | None
