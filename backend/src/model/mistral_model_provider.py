import json

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
        self.api_key = api_key

    def get_models(self) -> list[Model]:
        with Mistral(
            api_key=self.api_key,
        ) as mistral:
            unique_models = {}
            res = mistral.models.list()

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
        self, board: ConnectFourBoard, piece: PieceEnum, model_name: str
    ) -> Move | None:
        with Mistral(
            api_key=self.api_key,
        ) as mistral:
            system_prompt = self._get_system_prompt()
            prompt = self._create_prompt(board, piece)
            response = mistral.chat.complete(
                model=model_name,
                response_format={"type": "json_object"},
                messages=[system_prompt, prompt],
            )
            move = Move(**json.loads(str(response.choices[0].message.content)))
            return move

    def _create_prompt(self, board: ConnectFourBoard, piece: PieceEnum) -> UserMessage:
        s = f"CURRENT BOARD (0=empty, {piece}=YOU, {PieceEnum(3 - piece)}=OPPONENT):\n"
        s += "Col : 0 1 2 3 4 5 6\n"
        for i, r in enumerate(board.state):
            s += f"Row{i}: " + " ".join(map(str, r)) + "\n"

        moves = "\n".join(str(m.model_dump()) for m in board.get_possible_moves())

        s += f"""
Here are the possible moves you can make
{moves}

ANALYZE:
1. Can YOU win this turn? If yes, play that move.
2. Can OPPONENT win next turn? If yes, block that move.
3. Otherwise choose strategically.

Return ONLY: {{"col": integer, "row": integer}}
"""
        return UserMessage(content=s)

    def _parse_move_response(self, response) -> Move | None:
        try:
            content = response.choices[0].message.content
            col_str, row_str = content.strip().split(",")
            col = int(col_str)
            row = int(row_str)
            return Move(col=col, row=row)
        except Exception:
            return None

    def _get_system_prompt(self) -> SystemMessage:
        return SystemMessage(
            content="""You are an expert Connect Four player.

GAME RULES:
- 7 columns (numbered 0-6), 6 rows
- Pieces drop to the lowest empty row in chosen column
- Win by connecting 4 pieces horizontally, vertically, or diagonally
- You are piece 1, opponent is piece 2

STRATEGY (check in this order):
1. If YOU can win this turn, play that winning move
2. If OPPONENT can win next turn, block them
3. Otherwise, play strategically (center columns are strongest)

OUTPUT FORMAT:
Return ONLY valid JSON: {"col": integer, "row": integer}
No explanations. No other text.

EXAMPLES:
Example 1 - Take the win:
Board: Row5: 1 1 1 0 0 0 0
Analysis: You can win by playing column 3
Answer: {{"col": 3}}

Example 2 - Block opponent:
Board: Row5: 2 2 2 0 0 0 0
Analysis: Opponent wins if you don't block column 3
Answer: {{"col": 3, "row": 5}}

"""
        )

    def get_first_move(self, model_name: str) -> Move:
        # we might build a caching system for each model that maps model_name to a first move
        # for now, we just return a fixed first move
        return Move(col=0, row=5)
