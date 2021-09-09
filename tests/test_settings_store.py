from google.cloud import secretmanager

from dj_secret_settings.stores.from_json import JsonSettingsStore
from dj_secret_settings.stores.from_environment import EnvironmentSettingsStore
from dj_secret_settings.fetchers import from_gsm
from dj_secret_settings.settings_store import load


def test_no_config_returns_environment_store():
    store = load()
    assert isinstance(store, EnvironmentSettingsStore)


def test_json_config_returns_json_store(mocker):
    fetch = mocker.patch.object(from_gsm, "fetch", autospec=True)
    fetch.return_value = '{"key": 100}'
    store = load(
        "json+gsm://service_account@googleserviceaccount.com/projects/012345678/secrets/my-secret/versions/42"
    )
    assert isinstance(store, JsonSettingsStore)
    assert store.get_value("key") == 100


def test_environment_config_returns_environment_store():
    store = load("environment:")
    assert isinstance(store, EnvironmentSettingsStore)
