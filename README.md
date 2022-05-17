###

### Setup

Credentials can be provided in one of two ways:

1. Pass the credentials directly as a dictionary:

```python
from google_cloud.bigquery import BigQueryWork
class GetData(LightningFlow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = BigQueryWork()

    def run(
        self,
        project_id,
        columns,
        target,
        key,
    ):

        return self.client.run() self.stage_to_prod(
            columns=columns,
            source=staging_table,
            target=target,
            key=key,
        )

    def stage_to_prod(self, location="us-east1", project, columns, dataset, table):
        query = f"""
            select
                {','.join(columns)}
            from
                `{dataset}.{table}`
        """
        self.client.run(
            query=query, project=project, location=location
        )
```

2. Add a `contexts/.secrets.json` with the following information.
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
