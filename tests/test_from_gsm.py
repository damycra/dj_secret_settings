from google.cloud import secretmanager

from dj_secret_settings.fetchers.from_gsm import fetch


def test_path_clipped(mocker):
    mock_cls = mocker.patch.object(
        secretmanager, "SecretManagerServiceClient", autospec=True
    )

    secret_name = "path_that_is_actually_secret_name"
    fetch("dummy_service_account", f"/{secret_name}")

    client = mock_cls.return_value
    client.access_secret_version.assert_called_with({"name": secret_name})
