import os
import pickle
import time
from typing import List, Optional

import lightning as L
from google.cloud import bigquery
from google.oauth2.service_account import Credentials as SACredentials
from lightning.storage.path import Path


class BigQuery(L.LightningWork):
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
        sqlquery: str = None,
        project: Optional[str] = None,
        location: Optional[str] = "us-east1",
        data_dir: Optional[str] = None,
        credentials: Optional[dict] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.sqlquery = sqlquery
        self.project = project
        self.location = location
        self.result_path = Path(
            os.path.join(
                data_dir or self.LOCAL_STORE_DIR,
                ".".join([__name__, str(time.time()), "pkl"]),
            )
        )
        self.credentials = credentials

    def query(
        self,
        sqlquery: str,
        project: Optional[str] = None,
        location: Optional[str] = None,
        to_dataframe: Optional[bool] = False,
    ):
        self.run(
            sqlquery=sqlquery,
            project=project,
            location=location,
            to_dataframe=to_dataframe,
        )

    def insert(self, json_rows: List, table: str):
        self.run(json_rows=json_rows, table=table)

    def run(
        self,
        sqlquery: str = None,
        project: Optional[str] = None,
        location: Optional[str] = "us-east1",
        credentials: Optional[dict] = None,
        to_dataframe: Optional[bool] = False,
        json_rows: Optional[List] = None,
        table: Optional[str] = None,
    ) -> None:

        sqlquery = sqlquery or self.sqlquery
        project = project or self.project
        location = location or self.location
        credentials = credentials or self.credentials

        if sqlquery is None and json_rows is None:
            raise ValueError(
                f"`query` or `rows_to_insert` is required. Found: {sqlquery}"
            )

        if credentials is None:
            client = bigquery.Client(project=project)
        else:
            _credentials = SACredentials.from_service_account_info(
                credentials,
            )
            client = bigquery.Client(project=project, credentials=_credentials)

        if json_rows is not None:
            if table is None:
                raise AttributeError(
                    "Parameter `table` is required when json_rows is provided"
                    f"Instead target_table is {table}"
                )
            client.insert_rows_json(table=table, json_rows=json_rows)
            return

        cursor = client.query(sqlquery, location=location)

        if to_dataframe:
            result = cursor.result().to_dataframe()
        else:
            result = tuple(res.values() for res in cursor.result())

        with open(self.result_path, "wb") as _file:
            pickle.dump(result, _file)
