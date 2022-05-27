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

    To enable this:
    1. select an existing or create a new "project" https://console.cloud.google.com/projectselector2/home/
    2. enable billing for the project if it doesn't already have it
    3. enable the BigQuery API for the project at https://console.cloud.google.com/apis/library/bigquery.googleapis.com


    Example:
    .. code::python

    import lightning as L
    from lightning_bigquery.bigquery import BigQueryWork
    import pickle


    class ReadResults(L.LightningWork):
        def run(self, result_filepath):
            with open(result_filepath, "rb") as _file:
                data = pickle.load(_file)

                # Do something with the data
                data.head()


    class GetHackerNewsArticles(L.LightningFlow):
        def __init__(self, project, location, credentials):
            super().__init__()
            self.client = BigQueryWork(project=project, location=location, credentials=credentials)
            self.reader = ReadResults()

        def run(self):
            query = '''select title, score from `bigquery-public-data.hacker_news.stories` limit 5'''

            self.client.query(query, to_dataframe=True)
            if self.client.has_succeeded:
                self.reader.run(self.client.result_path)


    query: str, query that will be executed on BigQuery.
    project: str, the Google Cloud project that the BigQuery warehouse belongs to. Each Google Cloud Project
             can only have on BigQuery. To get your "project ID" go to the Google API Console
             https://console.cloud.google.com/bigquery, select the drop-down from the top navigation bar,
             and select your project ID.  By default, you're presented with the "RECENT" tab, navigate to the "ALL" tab
             to get a list of all projects you have access to in your organization.
             Compared to the more familiar database organized hierarchies like
             <DATABASE>.<SCHEMA>.<TABLE>; in BigQuery DATABASE="project", SCHEMA="dataset", and TABLE=table.
    region: str, this is referred to as a "location" in Google Cloud. To get this go to
            https://console.cloud.google.com/bigquery, select your "dataset", and from the pane that appears
            when the dataset is selected copy the value for "Data Location".
    credentials: dict, if no credentials are provided, and you've authenticated into google-cloud API through another
            mechanism (such as the google cloud cli) then those credentials will be used.  To get credentials that
            for automation scripts go to https://console.cloud.google.com/iam-admin/serviceaccounts > select the project
            and locate the service account you want to use > select "Manage keys" from the "Actions" column >
            select "ADD KEY" > "Create new key" > select "JSON" for key type and select "CREATE" > you'll receive a
            JSON file that can be used as a python dictionary.
    """

    LOCAL_STORE_DIR = Path(os.path.join(Path.home(), ".lightning-store"))

    def __init__(
        self,
        sqlquery: str = None,
        project: Optional[str] = None,
        location: Optional[str] = "us-east1",
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
                self.LOCAL_STORE_DIR,
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
        credentials: Optional[dict] = None,
        *args,
        **kwargs,
    ):
        self.run(
            sqlquery=sqlquery,
            project=project,
            location=location,
            to_dataframe=to_dataframe,
            credentials=credentials,
            *args,
            **kwargs,
        )

    def insert(self, json_rows: List, table: str, *args, **kwargs):
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

        cursor = client.query(sqlquery, location=location)

        if to_dataframe:
            result = cursor.result().to_dataframe()
        else:
            result = tuple(res.values() for res in cursor.result())

        with open(self.result_path, "wb") as _file:
            pickle.dump(result, _file)
