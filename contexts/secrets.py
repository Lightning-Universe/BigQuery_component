"""
TODO: Replace with a proper secrets management.
"""
import json
import os

from google.oauth2 import service_account

FILEPATH = os.path.join(os.path.dirname(__file__), ".secrets.json")
__SECRETS = json.load(open(FILEPATH))

LIGHTNING__BQ_SERVICE_ACCOUNT_CREDS = (
    service_account.Credentials.from_service_account_info(
        __SECRETS.get("google_service_account"),
    )
)
