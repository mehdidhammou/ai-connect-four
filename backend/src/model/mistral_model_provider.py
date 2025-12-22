import os

from mistralai import Mistral
from mistralai.models import UserMessage

from backend.src.types import move
from src.board.connect_four_board import ConnectFourBoard
from src.types.move import Move
from src.types.piece import Piece

from .model import Model
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
                    Model(
                        name=model["name"],
                        description=model_info.description or "",
                    ),
                )

        return list(unique_models.values())

    def get_move(
        self, board: ConnectFourBoard, piece: Piece, model_name: str
    ) -> Move | None:
        with Mistral(
            api_key=self.api_key,
        ) as mistral:
            prompt = self._create_prompt(board, piece)
            response = mistral.chat.complete(
                model=model_name,
                response_format={"type": "json_object"},
                messages=[prompt],
            )
            return self._parse_move_response(response.choices[0].message.content)

    def _create_prompt(self, board: ConnectFourBoard, piece: Piece) -> UserMessage:
        prompt = "Connect Four Board State:\n"
        for row in board.state:
            prompt += " | ".join(str(cell) for cell in row) + "\n"
        prompt += f"Player Piece: {piece}\n"
        prompt += 'Provide the next move as a JSON object in the format {"col": column_number, "row": row_number}.'
        return UserMessage(content=prompt)

    def _parse_move_response(self, response) -> Move | None:
        try:
            content = response.choices[0].message.content
            col_str, row_str = content.strip().split(",")
            col = int(col_str)
            row = int(row_str)
            return Move(col=col, row=row)
        except Exception:
            return None
