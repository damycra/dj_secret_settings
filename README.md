Yet Another Django Settings Helper
==================================

This package allows the source of some (or nearly all) settings to be easily changed for dev/Staging/Production etc purposes. e.g. One might obtain development settings from the process environment but later deploy to Google Compute Engine where use of Google Secret Manager is recommended. If the app later finds its way onto AWS, a suitable adaptor can be installed or written.

## Installation

    pip install dj_secret_settings

## Configuration

Install settings fetchers to get the raw data from the store, and settings stores to make sense of the raw data and return pieces of it on demand.

The package can be configured with a string or by using the environment variable `DJ_SECRET_SETTINGS_URL` with the form:

    store_type+fetcher_type://information.used.by/the/fetcher/and/or/the/store_type?like_a=url

e.g. `json+gsm://anything-here-perhaps-service-account/projects/123456789/secrets/my-secret/versions/42` indicates that data will be fetched from Google Secret Manager\* and interpreted as a JSON string.

\* configuration of this is obviously required too

## Usage

    from dj_secret_settings import settings_store
    store = settings.store.load("json+gsm://anything-here-perhaps-service-account/projects/123456789/secrets/my-secret/versions/42")

    MAX_SIZE = store.get_value('MAX_SIZE', default=314, coerce_type=int)

Other ways to get settings

    MY_LIST = store.get_array('MY_LIST')
    A_MAP = store.get_mapping('A_MAP', default={})
