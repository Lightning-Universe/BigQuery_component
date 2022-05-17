from google_cloud.bigquery import BigQueryWork
from unittest.mock import patch

@patch('google.cloud.bigquery.Client', autospec=True)
def test_query(mock_bigquery):
    mock_bigquery().query.return_value = ""
