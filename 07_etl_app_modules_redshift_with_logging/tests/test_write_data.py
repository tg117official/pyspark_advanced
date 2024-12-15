import os
import sys

import pytest
from unittest.mock import Mock
from pyspark.sql import SparkSession

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.write_data import write_to_redshift

@pytest.fixture
def spark():
    return SparkSession.builder \
        .appName("Test") \
        .master("local[*]") \
        .getOrCreate()

def test_write_to_redshift(spark, monkeypatch):
    # Mock input data
    clean_data = "mock_clean_data"
    conn_str = "mock_conn_str"
    table = "mock_table"
    user = "mock_user"

    # Mock DataFrame
    mock_df = Mock()
    monkeypatch.setattr(spark.read, "parquet", Mock(return_value=mock_df))
    mock_df.write.format = Mock(return_value=mock_df.write)
    mock_df.write.option = Mock(return_value=mock_df.write)

    # Run the write_to_redshift function
    write_to_redshift(spark, clean_data, conn_str, table, user)

    # Assertions
    spark.read.parquet.assert_called_once_with(clean_data)
    mock_df.write.format.assert_called_once_with("jdbc")
    mock_df.write.option.assert_any_call("url", conn_str)
    mock_df.write.option.assert_any_call("dbtable", table)
    mock_df.write.option.assert_any_call("user", user)
    mock_df.write.save.assert_called_once()
