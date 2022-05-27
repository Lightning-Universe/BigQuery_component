### About

This component gives you the ability to interface with gcp.

### Use the component

Run a query

```python
from typing import List
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
        query = """select title, score from `bigquery-public-data.hacker_news.stories` limit 5"""

        self.client.query(query, to_dataframe=True)
        if self.client.has_succeeded:
            self.reader.run(self.client.result_path)
```

### Install

```shell
git clone https://github.com/PyTorchLightning/google-cloud.git
cd lai-bigquery
pip install -e .
```

For mac users

```shell
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=true
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=true
git clone https://github.com/PyTorchLightning/google-cloud.git
cd lai-bigquery
pip install -e .
```
