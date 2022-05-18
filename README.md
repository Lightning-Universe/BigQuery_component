### About

This component gives you the ability to interface with gcp.

### Use the component

Credentials can be provided in one of two ways:

1. Pass the credentials directly as a dictionary:

```python
from typing import List
import lightning as L
from lightning_gcp.bigquery import BigQueryWork


class GetHackerNewsArticles(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.client = BigQueryWork()

    def run(
        self,
        location: str = "us-east1",
        project: str = "lightning",
        columns: List[str] = ["title", "score"],
        dataset: str = "",
        table: str = "",
        credentials: dict,
    ):
        query = f"""
            select
                {','.join(columns)}
            from
                `{dataset}.{table}`
        """

        # Result as a generator
        result = self.client.run(query=query, project=project, location=location, credentials=credentials)

        # Result as a dataframe
        result = self.client.run(
            query=query, project=project, location=location, credentials=credentials, to_dataframe=True
        )
```

2. Add or create `~/.lighning.secrets/.secrets.json` with the following information with passing credentials in as a run parameter.

```json
{
  "google_service_account": {
    "type": "service_account",
    "project_id": "<PROJECT_ID>",
    "private_key_id": "<PRIVATE_KEY_ID>",
    "private_key": "<PRIVATE_KEY>",
    "client_email": "<CLIENT_EMAIL>",
    "client_id": "<CLIENT_ID>",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "<CLIENT_CERT_URL>"
  }
}
```

### Install

```shell
git clone https://github.com/PyTorchLightning/google-cloud.git
cd google-cloud
pip install -e .
```
