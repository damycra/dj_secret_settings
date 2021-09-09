import json
import os

from typing import Any, Optional, Type
from collections.abc import Mapping, Sequence

from ..settings_store import DoNotCoerceBool, SettingsStore


class EnvironmentSettingsStore:
    def get_value(self, key: str, default=None, coerce_type: Type = None):
        if coerce_type and coerce_type is bool:
            raise DoNotCoerceBool("Use get_bool() instead")
        value: str = os.environ.get(key) or default
        return coerce_type(value) if coerce_type else value

    def get_bool(self, key: str, default: bool = False) -> bool:
        value = self.get_value(key, default)
        return (
            bool(value and value.lower() in ("true", "yes", "on", "1"))
            if value != default
            else default
        )

    def get_mapping(self, key: str, default: Mapping = None) -> Mapping:
        value = self.get_value(key, None)
        result = json.loads(value) if value else default
        if result is not None and not isinstance(result, Mapping):
            raise TypeError(
                f"Resulting value (from key: [{key}]) must be a mapping type"
            )
        return result

    def get_array(self, key: str, default: Sequence = None) -> Sequence:
        value = self.get_value(key, None)
        result = json.loads(value) if value else default
        if result is not None and (
            isinstance(result, str) or not isinstance(result, Sequence)
        ):  # error if it's a string
            raise TypeError(
                f"Resulting value (from key: [{key}]) must be a non-string sequence type"
            )
        return result


def get_store(data: Any, config: Optional[str] = None) -> SettingsStore:
    return EnvironmentSettingsStore()
