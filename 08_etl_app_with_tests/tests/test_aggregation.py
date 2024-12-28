import pytest
from pyspark.sql import SparkSession
from src.aggregations import perform_aggregations

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .appName("PySpark Unit Testing") \
        .master("local[*]") \
        .getOrCreate()

def test_perform_aggregations(spark):
    # Input DataFrame
    input_data = [
        (1, 100),
        (2, 200),
        (1, 300)
    ]
    schema = ["id", "amount"]
    input_df = spark.createDataFrame(input_data, schema)

    # Expected DataFrame
    expected_data = [
        (1, 400),
        (2, 200)
    ]
    expected_df = spark.createDataFrame(expected_data, ["id", "total_amount"])

    # Run perform_aggregations function
    aggregated_df = perform_aggregations(input_df)

    # Assert DataFrames are equal
    assert aggregated_df.collect() == expected_df.collect()
