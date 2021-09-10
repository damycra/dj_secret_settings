Yet Another Django Settings Helper
==================================

This library allows secret settings to be easily changed for dev/Staging/Production etc purposes. e.g. One might obtain development settings from the process environment but later deploy to _Google Compute Engine_ where use of *_Google Secret Manager_* is recommended. If the app later finds its way onto _AWS_, a suitable fetcher can be installed or written.

I tend to put all the secret settings for an environment in a single secret as a JSON document, for cost and convenience. You can also put non-secret settings in the same document or install them as environment variables as you prefer.

** I have no affiliation with Google, Amazon or any other cloud computing provider! **

## Installation

    pip install dj_secret_settings

## Configuration

Install settings fetchers to get the raw data from the store, and settings stores to make sense of the raw data and return pieces of it on demand.

The package can be configured with a string or by using the environment variable `DJ_SECRET_SETTINGS_URL` with the form:

    store_type+fetcher_type://information.used.by/the/fetcher/and/or/the/store_type?like_a=url

e.g. `json+gsm://anything-here-perhaps-service-account/projects/123456789/secrets/my-secret/versions/42` indicates that data will be fetched from _Google Secret Manager_\* and interpreted as a JSON string.

\* configuration of this is obviously required too, contact me if you need help with that.

The package includes a _Google Secret Manager_ fetcher, with JSON and environment variable store types. These can be overridden by installing a root package of the form dj_secret_settings_{store_type} (e.g. dj_secret_settings_json) or dj_secret_settings_{fetcher_type} (e.g dj_secret_settings_gsm). Alternatively you can install differently named root packages and modifiy the URL (e.g dj_secret_settings_yaml for a yaml store using the URL of the form yaml+gsm://...).

## Usage

    from dj_secret_settings import settings_store
    store = settings.store.load("json+gsm://anything-here-perhaps-service-account/projects/123456789/secrets/my-secret/versions/42")

    MAX_SIZE = store.get_value('MAX_SIZE', default=314, coerce_type=int)
    IS_PRODUCTION = store.get_boolean('is_production', default=FALSE)
    MY_LIST = store.get_array('MY_LIST')
    A_MAP = store.get_mapping('A_MAP', default={})

`default`s are always optional, as is `coerce_type` on `get_value`
