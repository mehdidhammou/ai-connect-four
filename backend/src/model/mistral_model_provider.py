import os

from mistralai import Mistral
from .model import Model

from .model_provider import ModelProvider


class MistralModelProvider(ModelProvider):
    def __init__(self, api_key: str):
        super().__init__(name="mistral")
        self.api_key = api_key

    def get_models(self) -> list[Model]:
        with Mistral(
            api_key=os.environ["MISTRAL_API_KEY"],
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
