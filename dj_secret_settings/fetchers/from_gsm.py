from dj_secret_settings.settings_store import NotInstalled


try:
    from google.cloud import secretmanager
except ImportError:
    raise NotInstalled(
        "Install Google Cloud secret manager; pip install google-cloud-secret-manager"
    )


def fetch(service_account: str, path: str, *args) -> str:
    name = path[1:]  # we do not want the leading / for a GSM secret name
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": name})

    return response.payload.data.decode()
