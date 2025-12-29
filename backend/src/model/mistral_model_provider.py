import json
import logging

from mistralai import Mistral
from mistralai.models import SystemMessage, UserMessage

from src.board.connect_four_board import ConnectFourBoard
from src.types.model import Model
from src.types.move import Move
from src.types.piece_enum import PieceEnum

from .model_provider import ModelProvider


class MistralModelProvider(ModelProvider):
    def __init__(self, api_key: str):
        super().__init__(name="mistral")
        self.client = Mistral(api_key=api_key)

    def get_models(self) -> list[Model]:
        unique_models = {}
        res = self.client.models.list()

        for model_info in res.data or []:
            model = {
                "name": model_info.id,
                "aliases": model_info.aliases,
            }
            key = tuple(sorted([model["name"], *model["aliases"]]))
            del model["aliases"]
            unique_models.setdefault(
                key,
                Model(name=model["name"]),
            )

        return list(unique_models.values())

    def get_move(
        self,
        board: ConnectFourBoard,
        piece: PieceEnum,
        model_name: str,
    ) -> Move | None:
        system_prompt = self._get_system_prompt(piece)
        prompt = self._create_prompt(board, piece)

        response = self.client.chat.complete(
            model=model_name,
            response_format={"type": "json_object"},
            messages=[system_prompt, prompt],
        )
        chosen_col = json.loads(str(response.choices[0].message.content))
        return board.get_move_from_col(chosen_col["col"])

    def _create_prompt(self, board: ConnectFourBoard, piece: PieceEnum) -> UserMessage:
        moves = "- " + "\n- ".join(
            str(m.model_dump()) for m in board.get_possible_moves()
        )
        return UserMessage(
            content=f"""
Board:
{board}

Possible moves:
{moves}
"""
        )

    def _get_system_prompt(self, piece: PieceEnum) -> SystemMessage:
        opponent_piece = PieceEnum(3 - piece)
        return SystemMessage(
            content=f"""
You are an expert Connect Four player.

GAME RULES:
- 7 columns (numbered 0-6), 6 rows
- Pieces drop to the lowest empty row in the chosen column
- Win by connecting 4 pieces horizontally, vertically, or diagonally
- You are piece {piece}, opponent is piece {opponent_piece}
- Always play a valid move (0-6).
- You are given a list of possible moves to choose from.

STRATEGY:
Choose one of the possible moves according to the following priority:
1. If YOU can win this turn, play that winning move
2. If OPPONENT can win next turn, block them

OUTPUT FORMAT:
Return ONLY valid JSON: {{"col": "integer"}}. No explanations, no other text.

EXAMPLES:

Example 1 - Take the win:
Board:
  0   1   2   3   4   5   6
| . | . | . | . | . | . | . |
| . | . | . | . | . | . | . |
| 2 | . | . | 2 | . | . | . |
| 2 | 2 | . | 1 | 2 | . | . |
| 1 | 1 | 1 | 2 | 1 | 2 | . |
| 1 | 1 | 2 | 1 | 1 | 1 | . |
Analysis: You can win diagonally by playing column 6
Answer: {{"col": 6}}

Example 2 - Block opponent:
Board:
  0   1   2   3   4   5   6
| . | . | . | . | . | . | . |
| . | . | . | . | . | . | . |
| . | . | . | . | . | . | . |
    | 1 | . | . | . | . | . | . |
| 1 | . | . | . | . | . | . |
| 1 | 2 | 2 | . | . | . | . |
Analysis: Opponent wins vertically if you don't block column 0
Answer: {{"col": 0}}
"""
        )

    def get_first_move(self, model_name: str) -> Move:
        # we might build a caching system for each model that maps model_name to a first move
        # for now, we just return a fixed first move
        return Move(col=0, row=5)
