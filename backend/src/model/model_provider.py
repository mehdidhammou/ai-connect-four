# abstract model provider class
from abc import ABC, abstractmethod

from .model import Model


class ModelProvider(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_models(self) -> list[Model]:
        pass
