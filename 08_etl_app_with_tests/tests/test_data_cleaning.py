import pytest
from pyspark.sql import SparkSession
from src.data_cleaning import clean_data

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .appName("PySpark Unit Testing") \
        .master("local[*]") \
        .getOrCreate()

def test_clean_data(spark):
    # Input DataFrame
    input_data = [
        (1, "John Doe", None),
        (2, None, "jane.doe@example.com")
    ]
    schema = ["id", "name", "email"]
    input_df = spark.createDataFrame(input_data, schema)

    # Expected DataFrame
    expected_data = [
        (1, "John Doe", "unknown"),
        (2, "unknown", "jane.doe@example.com")
    ]
    expected_df = spark.createDataFrame(expected_data, schema)

    # Run clean_data function
    clean_df = clean_data(input_df)

    # Assert DataFrames are equal
    assert clean_df.collect() == expected_df.collect()
