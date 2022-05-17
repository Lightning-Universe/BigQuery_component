"""
TODO: Replace with a proper secrets management.
"""
import json
import logging
import os
from pathlib import Path

from google.oauth2 import service_account

FILEPATH = os.path.join(str(Path.home()), ".lightning.secrets/.secrets.json")

try:
    __SECRETS = json.load(open(FILEPATH))
except FileNotFoundError as error:
    FILEPATH = os.path.join(os.path.dirname(__file__), ".qa.secrets.json")
    logging.error(f"{error}. Using {FILEPATH}.")
    __SECRETS = json.load(open(FILEPATH))

LIGHTNING__BQ_SERVICE_ACCOUNT_CREDS = (
    service_account.Credentials.from_service_account_info(
        __SECRETS.get("google_service_account"),
    )
)
