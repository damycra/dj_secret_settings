from json.decoder import JSONDecodeError
from typing import Mapping, Sequence
from dj_secret_settings.settings_store import DoNotCoerceBool
import pytest
from dj_secret_settings.stores.from_json import JsonSettingsStore, get_store


def test_get_store():
    store = get_store("{}")
    assert store is not None
    assert store.get_value("k", "dflt") == "dflt"


@pytest.mark.parametrize(
    "data",
    [
        '{"key: "foo"}',
        "{]",
        "unquoted text",
        '{"key": "bar" // comments not allowed}',
    ],
)
def test_fails_with_bad_json(data):
    with pytest.raises(JSONDecodeError):
        JsonSettingsStore(data)


@pytest.mark.parametrize(
    "data",
    [
        "1",
        '"quoted text"',
        "[1,2,3]",
    ],
)
def test_fails_with_bad_data(data):
    with pytest.raises(Exception):
        JsonSettingsStore(data)


@pytest.mark.parametrize(
    ["data", "expected"],
    [
        ('{"key": "foo"}', "foo"),
        ('{"key": true}', True),
        ('{"key": false}', False),
        ('{"key": "bar", "k2": "foo"}', "bar"),
    ],
)
def test_value_returned_if_present(data, expected):
    store = JsonSettingsStore(data)
    assert store.get_value("key") == expected


def test_none_returned_if_no_key_or_default():
    store = JsonSettingsStore('{"key": "foo"}')
    assert store.get_value("key2") is None


@pytest.mark.parametrize(
    ["data", "expected"],
    [
        ('{"key": "foo"}', "foo"),
        ('{"key": true}', True),
        ('{"key": false}', False),
        ('{"key": "bar", "k2": "foo"}', "bar"),
    ],
)
def test_default_not_returned_if_present(data, expected):
    store = JsonSettingsStore(data)
    assert store.get_value("key", "should not be returned") == expected


@pytest.mark.parametrize(
    "data",
    [
        '{"key": "foo"}',
        '{"key": true}',
        '{"key": false}',
        '{"key": "bar", "k2": "foo"}',
    ],
)
def test_default_returned_if_not_present(data):
    store = JsonSettingsStore(data)
    assert store.get_value("non-key", "dflt") == "dflt"


def test_bool_coerce_throws_error():
    store = JsonSettingsStore('{"key": "foo"}')
    with pytest.raises(DoNotCoerceBool):
        store.get_value("key", coerce_type=bool)


@pytest.mark.parametrize(
    ["data", "coerce", "expected"],
    [
        ('{"key": 10}', str, "10"),
        ('{"key": "11"}', int, 11),
        ('{"key": "list"}', list, ["l", "i", "s", "t"]),
    ],
)
def test_coerce_works(data, coerce, expected):
    store = JsonSettingsStore(data)
    assert store.get_value("key", coerce_type=coerce) == expected


@pytest.mark.parametrize(
    ["data", "coerce"],
    [
        ('{"key": "nan"}', int),
        ('{"key": 9}', list),
        ('{"key": [1,2,3]}', float),
    ],
)
def test_coerce_throws_error(data, coerce):
    store = JsonSettingsStore(data)
    with pytest.raises(Exception):
        store.get_value("key", coerce_type=coerce)


@pytest.mark.parametrize(
    "data",
    [
        '{"key": "true"}',
        '{"key": 1}',
        '{"key": [1,2,3]}',
        '{"key": {"k2": 4}}',
    ],
)
def test_non_bool_raises_error(data):
    store = JsonSettingsStore(data)
    with pytest.raises(TypeError):
        store.get_bool("key")


def test_true_value_evaluates_true():
    store = JsonSettingsStore('{"key": true}')
    assert store.get_bool("key") == True


def test_false_value_evaluates_true():
    store = JsonSettingsStore('{"key": false}')
    assert store.get_bool("key") == False


@pytest.mark.parametrize(
    "default",
    [
        None,
        1,
        [1, 2, 3],
        {"key": 4},
    ],
)
def test_non_bool_default_raises_error(default):
    store = JsonSettingsStore("{}")
    with pytest.raises(TypeError):
        store.get_bool("non-key", default)


@pytest.mark.parametrize(
    "default",
    [
        True,
        False,
    ],
)
def test_bool_default_ok(default):
    store = JsonSettingsStore("{}")
    assert store.get_bool("non-key", default) == default


def test_map_returned():
    store = JsonSettingsStore('{"key": {"map_key": 100}}')
    value = store.get_mapping("key")
    assert isinstance(value, Mapping)
    assert value["map_key"] == 100


def test_missing_map_key_returns_none():
    store = JsonSettingsStore("{}")
    assert store.get_mapping("non-key") is None


def test_non_map_default_raises_error():
    store = JsonSettingsStore("{}")
    with pytest.raises(TypeError):
        store.get_mapping("key", [1, 2, 3])


@pytest.mark.parametrize(
    "data",
    [
        '{"key": "text"}',
        '{"key": 20}',
        '{"key": [1,2,3]}',
        '{"key": true}',
    ],
)
def test_non_mapping_raises_error(data):
    store = JsonSettingsStore(data)
    with pytest.raises(TypeError):
        store.get_mapping("key")


def test_list_returned():
    store = JsonSettingsStore('{"key": [1,2,3]}')
    value = store.get_array("key")
    assert isinstance(value, Sequence)
    assert value[1] == 2


def test_missing_list_key_returns_none():
    store = JsonSettingsStore("{}")
    assert store.get_array("non-key") is None


def test_non_list_default_raises_error():
    store = JsonSettingsStore("{}")
    with pytest.raises(TypeError):
        store.get_array("key", "non list")


@pytest.mark.parametrize(
    "data",
    [
        '{"key": "text"}',
        '{"key": 20}',
        '{"key": {"mk": [2,3]}}',
        '{"key": true}',
    ],
)
def test_non_array_raises_error(data):
    store = JsonSettingsStore(data)
    with pytest.raises(TypeError):
        store.get_array("key")
