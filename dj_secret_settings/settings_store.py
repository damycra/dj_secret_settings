import importlib

from collections.abc import Mapping, Sequence

from typing import Any, Optional, Type

try:
    from typing import Protocol  # 3.8+
except ImportError:

    class Protocol:
        pass


from urllib.parse import urlparse


class NotInstalled(Exception):
    pass


class DoNotCoerceBool(Exception):
    pass


class BadData(Exception):
    pass


class SettingsStore(Protocol):
    def get_value(self, key: str, default=None, coerce_type: Type = None):
        pass

    def get_bool(self, key: str, default: bool = False) -> bool:
        pass

    def get_mapping(self, key: str, default: Mapping = None) -> Mapping:
        pass

    def get_array(self, key: str, default: Sequence = None) -> Sequence:
        pass


def _get_fetcher_module(fetcher_type: str):
    try:
        module = importlib.import_module(f"dj_secret_settings_{fetcher_type}")
    except ImportError as ie:
        try:
            module = importlib.import_module(
                f".fetchers.from_{fetcher_type}", package=__package__
            )
        except ImportError:
            raise NotInstalled(
                f"If [{fetcher_type}] is correct, install or implement dj_secret_settings_{fetcher_type}"
            ) from ie
    return module


def _get_store_factory(store_type: str):
    try:
        module = importlib.import_module(f"dj_secret_settings_{store_type}")
    except ImportError as ie:
        try:
            module = importlib.import_module(
                f".stores.from_{store_type}", package=__package__
            )
        except ImportError:
            raise NotInstalled(
                f"If [{store_type}] is correct, install or implement dj_secret_settings_{store_type}"
            ) from ie
    return module.get_store


def _get_store(config: str):
    parsed = urlparse(config)
    store_type, *rest = parsed.scheme.split("+")

    if rest:
        fetcher_type = rest[0]
        fetcher = _get_fetcher_module(fetcher_type)
        data = fetcher.fetch(*parsed[1:])
    else:
        data = None

    store_factory = _get_store_factory(store_type)
    # pass entire config in case implementation wants to do everything
    return store_factory(data, config=config)


def load(config: Optional[str] = None) -> SettingsStore:
    """
    @param config e.g. json+gsm://service_account@googleserviceaccount.com/projects/012345678/secrets/my-secret/versions/42
    """
    if not config:  # load from environment
        import os

        config = os.environ.get("DJ_SECRET_SETTINGS_URL")
    if config and not config.lower().startswith("environment://"):
        result = _get_store(config)
    else:
        from .stores import from_environment

        result = from_environment.EnvironmentSettingsStore()

    return result
