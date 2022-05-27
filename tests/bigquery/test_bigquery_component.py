import json
import os
import pickle
from unittest.mock import patch

import lightning as L
import pandas as pd
from google.cloud import bigquery as bq
from lightning.runners import MultiProcessRuntime
from lightning.storage.path import Path

from lightning_bigquery import BigQuery

path = Path(os.path.join(Path.home(), ".lightning-store"))
if not os.path.exists(path):
    os.makedirs(path)


@patch("google.cloud.bigquery.Client", autospec=True)
def test_instantiation(mock_bigquery):
    """Test that the work can get instantiated."""
    work = BigQuery(
        sqlquery="""select 2""",
        project="lightning",
        location="us-east1",
    )

    expected = """select 2"""
    actual = work.sqlquery

    assert expected == actual


class MockResult(tuple):
    def values(self):
        return (("foo", "bar"),)

    def to_dataframe(self):
        return pd.DataFrame(columns=[1, 2], data=[["foo", "bar"]])


class MockQuery:
    def result(self):
        return MockResult()


def test_get_dataframe():

    with patch.object(bq.Client, "query", return_value=MockQuery()) as _:
        work = BigQuery()
        work.query(
            sqlquery="""select 2""",
            project="project",
            location="us-east1",
            to_dataframe=True,
        )
        with open(work.result_path, "rb") as _file:
            result = pickle.load(_file)

        expected = type(pd.DataFrame())
        actual = type(result)
        assert expected == actual


class ReaderWork(L.LightningWork):
    def run(self, data_source_path: str):
        expected = pd.DataFrame(columns=[1, 2], data=[["foo", "bar"]])
        not_expected = pd.DataFrame(columns=[1, 3], data=[["foo", "bar"]])
        with open(data_source_path, "rb") as _file:
            actual = pickle.load(_file)

        assert actual.equals(expected)
        assert not (actual.equals(not_expected))


class PatchedBigQuery(BigQuery):
    def query(self, *args, **kwargs):
        with patch.object(bq.Client, "query", return_value=MockQuery()) as _:
            super().query(*args, **kwargs)


class BQReader(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.client = PatchedBigQuery()
        self.reader = ReaderWork()

    def run(self):

        _fp = os.path.join(os.path.dirname(__file__), "../.qa.secrets.json")
        with open(_fp) as _file:
            credentials = json.load(_file)

        self.client.run(
            sqlquery="fakequery",
            project="project",
            location="us-east-1",
            to_dataframe=True,
            credentials=credentials,
        )

        if self.client.has_succeeded:

            assert Path(self.client.result_path).is_file()

            self.reader.run(self.client.result_path)

            print(self.reader.has_succeeded)
            if self.reader.has_succeeded:
                self._exit()


def xtest_query_from_app():
    """Test that the BQ work runs end-to-end in a typical app flow."""
    app = L.LightningApp(BQReader(), debug=True)
    MultiProcessRuntime(app, start_server=False).dispatch()
