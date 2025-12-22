from .heuristic import Heuristic
from src.types.heuristic_enum import HeuristicEnum


class HeuristicFactory:
    _providers = {}

    @classmethod
    def register(cls, name: HeuristicEnum, heuristic_cls):
        cls._providers[name] = heuristic_cls

    @classmethod
    def create(cls, name: HeuristicEnum) -> Heuristic:
        heuristic_cls = cls._providers.get(name)

        if not heuristic_cls:
            raise ValueError(f"Unknown heuristic: {name}")
        return heuristic_cls()
