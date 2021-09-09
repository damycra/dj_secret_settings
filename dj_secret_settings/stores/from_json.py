import json
import os

from typing import Any, Optional, Type
from collections.abc import Mapping, Sequence

from ..settings_store import BadData, DoNotCoerceBool, SettingsStore


class JsonSettingsStore:
    """
    A settings store created from a JSON encoded string
    """

    data: dict

    def __init__(self, encoded_data: str):
        self.data = json.loads(encoded_data)
        if not isinstance(self.data, Mapping):
            raise BadData("Data must be a JSON dictionary")

    def get_value(self, key: str, default=None, coerce_type: Type = None):
        if coerce_type and coerce_type is bool:
            raise DoNotCoerceBool("Use get_bool() instead")
        value: str = self.data.get(key, default)
        return coerce_type(value) if coerce_type else value

    def get_bool(self, key: str, default: bool = False) -> bool:
        value = self.data.get(key, default)
        # WILL return true for 'false'? test and eliminate TODO
        return (
            bool(
                (
                    value.lower() in ("true", "yes", "on", "1")
                    if isinstance(value, str)
                    else value
                )
            )
            if value != default
            else default
        )

    def get_mapping(self, key: str, default: Mapping = None) -> Mapping:
        value = self.data.get(key) or default
        if value and not isinstance(value, Mapping):
            raise TypeError(
                f"Resulting value (from key: [{key}]) must be a mapping type"
            )
        return value

    def get_array(self, key: str, default: Sequence = None) -> Sequence:
        value = self.data.get(key) or default
        if value and (
            isinstance(value, str) or not isinstance(value, Sequence)
        ):  # error if it's a string
            raise TypeError(
                f"Resulting value (from key: [{key}]) must be a non-string sequence type"
            )
        return value


def get_store(data: Any, config: Optional[str] = None) -> SettingsStore:
    return JsonSettingsStore(data)
