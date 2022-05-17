from typing import Optional

import lightning as L
from google.cloud import bigquery

import contexts


class BigQueryWork(L.LightningWork):
    """Task for running queries on BigQuery.

    Args:
        query: str, query that will be executed on BigQuery.
        project: str, the project identifier that BigQuery dataset exists in. Default = None.
        location: str, the location that the BigQuery dataset exists in.

    Example:

    .. code:: python

    """

    def __init__(
        self,
        query: str = None,
        project: Optional[str] = None,
        location: Optional[str] = "us-east1",
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.query = query
        self.project = project
        self.location = location
        self.result = None

    def run(
        self,
        query: str = None,
        project: Optional[str] = None,
        location: Optional[str] = "us-east1",
        credentials: Optional[dict] = contexts.secrets.LIGHTNING__BQ_SERVICE_ACCOUNT_CREDS,
        to_dataframe: Optional[bool] =False,
    ) -> None:

        if query is None:
            raise ValueError(f"Expected valid BigQuery SQL query. Observed: {query}")

        if credentials is None:
            client = bigquery.Client(project=project)
        else:
            client = bigquery.Client(project=project, credentials=credentials)

        cursor = client.query(query, location=location)

        if to_dataframe:
            self.result = cursor.result().to_dataframe()
        else:
            self.result = list(cursor.result())[0].values()
