from enum import Enum, auto


class GameState(Enum):
    WIN = "You win!"
    LOSE = "You lose!"
    TIE = "It's a tie!"
    CONTINUE = "Continue"
    MM_POS_WIN = "Positions heuristic wins!"
    MM_PIECE_WIN = "Pieces heuristic wins!"
