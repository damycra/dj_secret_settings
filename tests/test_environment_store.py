from json.decoder import JSONDecodeError
from typing import Mapping, Sequence
from dj_secret_settings.settings_store import DoNotCoerceBool
import pytest

from os import environ

from dj_secret_settings.stores.from_environment import EnvironmentSettingsStore


@pytest.mark.parametrize(
    ["mocker", "data", "expected"],
    [
        ("mocker", {"key": "foo"}, "foo"),
        ("mocker", {"key": "true"}, "true"),
        ("mocker", {"key": "false"}, "false"),
        ("mocker", {"key": "33"}, "33"),
    ],
    indirect=["mocker"],
)
def test_value_returned_if_present(mocker, data, expected):
    mocker.patch.dict(environ, data)
    store = EnvironmentSettingsStore()

    assert store.get_value("key") == expected


def test_none_returned_if_no_key_or_default(mocker):
    mocker.patch.dict(environ, {"key": "foo"})
    store = EnvironmentSettingsStore()
    assert store.get_value("key2") is None


@pytest.mark.parametrize(
    ["mocker", "data", "expected"],
    [
        ("mocker", {"key": "foo"}, "foo"),
        ("mocker", {"key": "bar", "k2": "foo"}, "bar"),
    ],
    indirect=["mocker"],
)
def test_default_not_returned_if_present(mocker, data, expected):
    mocker.patch.dict(environ, data)
    store = EnvironmentSettingsStore()
    assert store.get_value("key", "should not be returned") == expected


@pytest.mark.parametrize(
    ["mocker", "data"],
    [
        ("mocker", {"key": "foo"}),
        ("mocker", {"key": "bar", "k2": "foo"}),
    ],
    indirect=["mocker"],
)
def test_default_returned_if_not_present(mocker, data):
    mocker.patch.dict(environ, data)
    store = EnvironmentSettingsStore()
    assert store.get_value("non-key", "dflt") == "dflt"


def test_bool_coerce_throws_error(mocker):
    mocker.patch.dict(environ, {"key": "foo"})
    store = EnvironmentSettingsStore()
    with pytest.raises(DoNotCoerceBool):
        store.get_value("key", coerce_type=bool)


@pytest.mark.parametrize(
    ["mocker", "data", "coerce", "expected"],
    [
        ("mocker", {"key": "10"}, str, "10"),
        ("mocker", {"key": "11"}, int, 11),
        ("mocker", {"key": "list"}, list, ["l", "i", "s", "t"]),
    ],
    indirect=["mocker"],
)
def test_coerce_works(mocker, data, coerce, expected):
    mocker.patch.dict(environ, data)
    store = EnvironmentSettingsStore()
    assert store.get_value("key", coerce_type=coerce) == expected


@pytest.mark.parametrize(
    ["mocker", "data", "coerce"],
    [
        ("mocker", {"key": "nan"}, int),
        ("mocker", {"key": "[1,2,3]"}, float),
    ],
    indirect=["mocker"],
)
def test_coerce_throws_error(mocker, data, coerce):
    mocker.patch.dict(environ, data)
    store = EnvironmentSettingsStore()
    with pytest.raises(Exception):
        store.get_value("key", coerce_type=coerce)


@pytest.mark.parametrize(
    ["mocker", "data"],
    [
        ("mocker", {"key": "true"}),
        ("mocker", {"key": "1"}),
        ("mocker", {"key": "on"}),
        ("mocker", {"key": "yes"}),
    ],
    indirect=["mocker"],
)
def test_true_string_evaluates_true(mocker, data):
    mocker.patch.dict(environ, data)
    store = EnvironmentSettingsStore()
    assert store.get_bool("key") == True


@pytest.mark.parametrize(
    ["mocker", "data"],
    [
        ("mocker", {"key": "false"}),
        ("mocker", {"key": "0"}),
        ("mocker", {"key": "no"}),
        ("mocker", {"key": "off"}),
        ("mocker", {"key": "anything"}),
    ],
    indirect=["mocker"],
)
def test_false_string_evaluates_false(mocker, data):
    mocker.patch.dict(environ, data)
    store = EnvironmentSettingsStore()
    assert store.get_bool("key", default=True) == False


def test_map_returned(mocker):
    mocker.patch.dict(environ, {"key": '{"map_key": 100}'})
    store = EnvironmentSettingsStore()
    value = store.get_mapping("key")
    assert isinstance(value, Mapping)
    assert value["map_key"] == 100


def test_missing_map_key_returns_none():
    store = EnvironmentSettingsStore()
    assert store.get_mapping("non-key") is None


def test_non_map_default_raises_error():
    store = EnvironmentSettingsStore()
    with pytest.raises(TypeError):
        store.get_mapping("key", [1, 2, 3])


def test_non_mapping_raises_error(mocker):
    mocker.patch.dict(environ, {"key": "text"})
    store = EnvironmentSettingsStore()
    with pytest.raises((TypeError, JSONDecodeError)):
        store.get_mapping("key")


def test_list_returned(mocker):
    mocker.patch.dict(environ, {"key": "[1,2,3]"})
    store = EnvironmentSettingsStore()
    value = store.get_array("key")
    assert isinstance(value, Sequence)
    assert value[1] == 2


def test_missing_list_key_returns_none():
    store = EnvironmentSettingsStore()
    assert store.get_array("non-key") is None


def test_non_list_default_raises_error():
    store = EnvironmentSettingsStore()
    with pytest.raises(TypeError):
        store.get_array("key", "non list")


@pytest.mark.parametrize(
    ["mocker", "data"],
    [
        ("mocker", {"key": "text"}),
        ("mocker", {"key": "{}"}),
    ],
    indirect=["mocker"],
)
def test_non_array_raises_error(mocker, data):
    mocker.patch.dict(environ, data)
    store = EnvironmentSettingsStore()
    with pytest.raises((TypeError, JSONDecodeError)):
        store.get_array("key")
