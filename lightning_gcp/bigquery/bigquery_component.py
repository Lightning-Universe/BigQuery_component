import os
import pickle
import time
from typing import Optional

import lightning as L
from google.cloud import bigquery
from lightning.storage.path import Path

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

    LOCAL_STORE_DIR = Path(os.path.join(Path.home(), ".lightning-store"))

    def __init__(
        self,
        query: str = None,
        project: Optional[str] = None,
        location: Optional[str] = "us-east1",
        data_dir: Optional[str] = None,
    ):
        super().__init__()
        self.query = query
        self.project = project
        self.location = location
        self.result_path = Path(
            os.path.join(
                data_dir or self.LOCAL_STORE_DIR,
                ".".join([__name__, str(time.time()), "pkl"]),
            )
        )

    def run(
        self,
        query: str = None,
        project: Optional[str] = None,
        location: Optional[str] = "us-east1",
        credentials: Optional[
            dict
        ] = contexts.secrets.LIGHTNING__BQ_SERVICE_ACCOUNT_CREDS,
        to_dataframe: Optional[bool] = False,
    ) -> None:

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
            result = cursor.result().to_dataframe()
        else:
            result = tuple(res.values() for res in cursor.result())

        with open(self.result_path, "wb") as _file:
            pickle.dump(result, _file)
