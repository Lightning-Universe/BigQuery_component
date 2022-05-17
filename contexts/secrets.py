"""
TODO: Replace with a proper secrets management.
"""
import json
import logging
import os

from google.oauth2 import service_account

FILEPATH = os.path.join(os.path.dirname(__file__), ".secret.json")

try:
    __SECRETS = json.load(open(FILEPATH))
except FileNotFoundError as error:
    logging.error(f"{error}. Instead loading.")
    __SECRETS = json.load(open(os.path.join(os.path.dirname(__file__), ".qa.secrets.json")))

LIGHTNING__BQ_SERVICE_ACCOUNT_CREDS = (
    service_account.Credentials.from_service_account_info(
        __SECRETS.get("google_service_account"),
    )
)
