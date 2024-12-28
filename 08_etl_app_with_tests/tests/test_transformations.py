import pytest
from pyspark.sql import SparkSession
from src.transformations import apply_transformations

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .appName("PySpark Unit Testing") \
        .master("local[*]") \
        .getOrCreate()

def test_apply_transformations(spark):
    # Input DataFrame
    input_data = [
        (1, "John", 100),
        (2, "Jane", 200)
    ]
    schema = ["id", "name", "amount"]
    input_df = spark.createDataFrame(input_data, schema)

    # Expected DataFrame
    expected_data = [
        (1, "JOHN", 1000),
        (2, "JANE", 2000)
    ]
    expected_df = spark.createDataFrame(expected_data, schema)

    # Run apply_transformations function
    transformed_df = apply_transformations(input_df)

    # Assert DataFrames are equal
    assert transformed_df.collect() == expected_df.collect()
