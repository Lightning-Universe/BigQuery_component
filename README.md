<!---:lai-name: BigQuery--->
<div align="center">
<img src="static/big-query-icon.png" width="200px">

    A Lightning component to run queries on BigQuery.
    ______________________________________________________________________

![Tests](https://github.com/PyTorchLightning/LAI-bigquery/actions/workflows/ci-testing.yml/badge.svg)
</div>

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
        project: str = "bigquery-public-data",
        columns: List[str] = ["title", "score"],
        dataset: str = "hacker_news",
        table: str = "stories",
        credentials: dict,
    ):
        query = f"""
            select
                {','.join(columns)}
            from
                `{dataset}.{table}`
        """

        self.client.run(query=query, project=project, location=location, credentials=credentials)

        # The data will be stored in the works result path as tuple serialized in a pickled file.
        # To use it in another work, deserialize it as follows.
        # with open(self.client.result_path, 'rb') as _file:
        #   data = pickle.load(_file)
        self.client.result_path

        self.client.run(query=query, project=project, location=location, credentials=credentials, to_dataframe=True)
        # The data will be stored in the works result path as a pandas DataFrame in a pickled file.
        # To use it in another work, deserialize it as follows.
        # with open(self.client.result_path, 'rb') as _file:
        #   data = pickle.load(_file)
        self.client.result_path
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
