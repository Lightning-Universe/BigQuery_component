<!---:lai-name: BigQuery--->

<div align="center">
<img src="static/big-query-icon.png" width="200px">

```
A Lightning component to run queries on BigQuery.
______________________________________________________________________
```

![Tests](https://github.com/PyTorchLightning/LAI-bigquery/actions/workflows/ci-testing.yml/badge.svg)

</div>

### About

This component lets you run queries against a BigQuery warehouse.

### Use the component

To Run a query

```python
import pickle
import lightning as L
from lightning_bigquery import BigQuery


class YourComponent(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.bq_client = BigQuery(
            project="<YOUR GOOGLE PROJECT ID>",
            location="<LOCATION OF DATASET>",  # Region where the dataset is located.
            credential="<SERVICE ACCOUNT KEY>",  # Service account credentials
        )
        self.reader = ReadResults()

    def run(self):
        query = "select * from <BigQuery table>"
        self.bq_client.query(query, to_dataframe=True)

        if self.bq_client.has_succeeded:
            # The results from the query are saved as a pickled file.
            self.reader.run(self.bq_client.result_path)


class ReadResults(L.LightningWork):
    def run(self, result_filepath):
        with open(result_filepath, "rb") as _file:
            data = pickle.load(_file)

        # Print top results from the dataframe
        print(data.head())


app = L.LightningApp(YourComponent())
```

### Install

Run the following to install:

```shell
git clone https://github.com/PyTorchLightning/LAI-bigquery
cd LAI-bigquery
pip install -r requirements.txt
pip install -e .
```

### Tests

To run unit tests locally:

```shell
# From the root level of the package (LAI-bigquery)
pip install -r tests/requirements.txt
pytest
```
