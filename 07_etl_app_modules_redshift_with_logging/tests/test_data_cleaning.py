import os
import sys

import pytest
from unittest.mock import Mock
from pyspark.sql import SparkSession

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.data_cleaning import clean_data

@pytest.fixture
def spark():
    return SparkSession.builder \
        .appName("Test") \
        .master("local[*]") \
        .getOrCreate()

def test_clean_data(spark, monkeypatch):
    # Mock input and output paths
    input_path = "mock_input_path"
    output_path = "mock_output_path"

    # Mock DataFrame
    input_data = [("John", None), ("Alice", "Doe"), ("John", None)]
    schema = ["first_name", "last_name"]
    mock_df = spark.createDataFrame(input_data, schema)

    # Mock Spark read and write operations
    monkeypatch.setattr(spark.read, "csv", Mock(return_value=mock_df))
    mock_df.dropna = Mock(return_value=mock_df.dropna())
    mock_df.dropDuplicates = Mock(return_value=mock_df.dropDuplicates())
    mock_df.write = Mock()

    # Run the clean_data function
    clean_data(spark, input_path, output_path)

    # Assertions
    spark.read.csv.assert_called_once_with(input_path, header=True, inferSchema=True)
    mock_df.dropna.assert_called_once()
    mock_df.dropDuplicates.assert_called_once()
    mock_df.write.mode.assert_called_once_with("overwrite")
