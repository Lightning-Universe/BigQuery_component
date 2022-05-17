from unittest.mock import patch

from google.cloud import bigquery

from lightning_gcp.bigquery import BigQueryWork


@patch("google.cloud.bigquery.Client", autospec=True)
def test_instantiation(mock_bigquery):
    """Test that the work can get instantiated."""
    work = BigQueryWork()
    work.run(
        query="""select 2""",
        project="grid-analytics-processes-prod",
        location="us-east1",
    )
    expected = []
    actual = work.result

    assert expected == actual


class MockResult(tuple):
    def values(self):
        return ("foo", "bar")


def test_query():
    class MockQuery:
        def result(self):
            yield MockResult()

    with patch.object(bigquery.Client, "query", return_value=MockQuery()) as _:

        work = BigQueryWork()
        work.run(query="""select 2""", project="project", location="us-east1")
        expected = ("foo", "bar")
        actual = work.result
        assert expected == actual
