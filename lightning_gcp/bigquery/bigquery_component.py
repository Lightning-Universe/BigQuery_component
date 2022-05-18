from typing import Optional

import lightning as L
import pandas as pd
from google.cloud import bigquery

import contexts


class BigQueryWork(L.LightningWork):
    """Task for running queries on BigQuery.

    Args:
        query: str, query that will be executed on BigQuery.
        project: str, the project identifier that BigQuery dataset exists in.
                 Default = None.
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

    def run(
        self,
        query: str = None,
        project: Optional[str] = None,
        location: Optional[str] = "us-east1",
        credentials: Optional[
            dict
        ] = contexts.secrets.LIGHTNING__BQ_SERVICE_ACCOUNT_CREDS,
        to_dataframe: Optional[bool] = False,
    ) -> pd.DataFrame or bigquery.client.Client.query:

        self.query = query or self.query
        self.project = project or self.project
        self.location = location or self.location

        if self.query is None:
            raise ValueError(f"SQL query is required. Observed: {self.query}")

        if credentials is None:
            client = bigquery.Client(project=project)
        else:
            client = bigquery.Client(project=project, credentials=credentials)

        cursor = client.query(self.query, location=location)

        if to_dataframe:
            return cursor.result().to_dataframe()
        else:
            return cursor
