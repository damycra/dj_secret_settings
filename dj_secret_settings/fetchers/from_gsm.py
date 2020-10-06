from google.cloud import secretmanager


def fetch(service_account: str, path: str, *args) -> str:
    name = path[1:]  # we do not want the leading / for a GSM secret name
    client = secretmanager.SecretManagerServiceClient()

    response = client.access_secret_version(request={"name": name})

    return response.payload.data.decode()
