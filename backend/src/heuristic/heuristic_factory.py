from .heuristic import Heuristic


class HeuristicFactory:
    _providers = {}

    @classmethod
    def register(cls, name, heuristic_cls, *args, **kwargs):
        cls._providers[name] = {"cls": heuristic_cls, "args": args, "kwargs": kwargs}

    @classmethod
    def create(cls, name) -> Heuristic:
        entry = cls._providers.get(name)

        if not entry:
            raise ValueError(f"Unknown heuristic: {name}")

        heuristic_cls = entry["cls"]
        args = entry["args"]
        kwargs = entry["kwargs"]
        return heuristic_cls(*args, **kwargs)
