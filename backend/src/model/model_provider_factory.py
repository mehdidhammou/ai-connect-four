from src.types.model_provider_name import ModelProviderName

from .model_provider import ModelProvider


class ModelProviderFactory:
    _providers = {}

    @classmethod
    def register(cls, name: ModelProviderName, provider_cls, *args, **kwargs):
        cls._providers[name] = {"cls": provider_cls, "args": args, "kwargs": kwargs}

    @classmethod
    def create(cls, name: ModelProviderName) -> ModelProvider:
        entry = cls._providers.get(name)

        if not entry:
            raise ValueError(f"Unknown provider: {name}")

        provider_cls = entry["cls"]
        args = entry["args"]
        kwargs = entry["kwargs"]
        return provider_cls(*args, **kwargs)
