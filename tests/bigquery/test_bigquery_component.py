import pickle
from unittest.mock import patch

import pandas as pd
from google.cloud import bigquery

from lightning_gcp.bigquery import BigQueryWork


@patch("google.cloud.bigquery.Client", autospec=True)
def test_instantiation(mock_bigquery):
    """Test that the work can get instantiated."""
    work = BigQueryWork(
        query="""select 2""",
        project="lightning",
        location="us-east1",
    )

    expected = """select 2"""
    actual = work.query

    assert expected == actual


class MockResult(tuple):
    def values(self):
        return (("foo", "bar"),)

    def to_dataframe(self):
        return pd.DataFrame(columns=[1, 2], data=[["foo", "bar"]])


def test_query():
    class MockQuery:
        def result(self):
            yield MockResult()

    with patch.object(bigquery.Client, "query", return_value=MockQuery()) as _:

        work = BigQueryWork()
        work.run(query="fakequery", project="a", location="loc")
        with open(work.result_path, "rb") as _file:
            data = pickle.load(_file)

        expected = ("foo", "bar")
        actual = data[0][0]
        assert expected == actual


def test_get_dataframe():
    class MockQuery:
        def result(self):
            return MockResult()

    with patch.object(bigquery.Client, "query", return_value=MockQuery()) as _:
        work = BigQueryWork()
        work.run(
            query="""select 2""",
            project="project",
            location="us-east1",
            to_dataframe=True,
        )
        with open(work.result_path, "rb") as _file:
            result = pickle.load(_file)

        expected = type(pd.DataFrame())
        actual = type(result)
        assert expected == actual
