import pytest
from pyspark.sql import SparkSession
from src.data_cleaning import clean_data
from src.transformations import apply_transformations
from src.aggregations import perform_aggregations
from src.utils import load_schema


import sys
import os

# Ensure src is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
@pytest.fixture(scope="module")
def spark():
    """Initialize a local Spark session for testing."""
    return SparkSession.builder.master("local").appName("ETL Test").getOrCreate()

def test_etl_pipeline(spark, tmp_path):
    """Tests the full ETL pipeline."""
    # Define file paths
    input_path = str(tmp_path / "input.csv")
    clean_data_path = str(tmp_path / "clean_data.parquet")
    transformed_data_path = str(tmp_path / "transformed_data.parquet")
    aggregated_data_path = str(tmp_path / "aggregated_data.parquet")
    schema_path = str(tmp_path / "schema.json")

    # Mock schema JSON file
    schema_content = """
{
  "fields": [
    {"name": "id", "type": "int", "nullable": true},
    {"name": "first_name", "type": "string", "nullable": true},
    {"name": "last_name", "type": "string", "nullable": true},
    {"name": "email", "type": "string", "nullable": true},
    {"name": "dept", "type": "string", "nullable": true},
    {"name": "salary", "type": "double", "nullable": true}
  ]
}
    """
    schema_path_obj = tmp_path / "schema.json"
    schema_path_obj.write_text(schema_content)

    # Load schema
    schema = load_schema(schema_path)

    # Create input CSV file
    input_data = """id,first_name,last_name,email,dept,salary
1,Martica,Anglin,manglin0@stanford.edu,Human Resources,9
2,Jaime,Wikey,jwikey1@clickbank.net,Human Resources,13
3,Perice,Papes,ppapes2@trellian.com,Engineering,12
4,Adrianne,Blissitt,ablissitt3@ebay.com,Legal,7
5,Trenton,Elcox,telcox4@google.cn,Legal,21
6,Ryann,Bilson,rbilson5@desdev.cn,Product Management,11
7,Drew,Feather,dfeather6@amazon.co.jp,Research and Development,22"""
    input_path_obj = tmp_path / "input.csv"
    input_path_obj.write_text(input_data)

    # Step 1: Data Cleaning
    clean_data(spark, input_path, clean_data_path, schema_path)
    clean_df = spark.read.parquet(clean_data_path)
    assert clean_df.count() == 7  # Ensure data was properly cleaned

    # Step 2: Transformations
    apply_transformations(spark, clean_data_path, transformed_data_path, schema_path)
    transformed_df = spark.read.parquet(transformed_data_path)
    assert "avg_salary" in transformed_df.columns  # Verify transformation success

    # Step 3: Aggregations
    perform_aggregations(spark, transformed_data_path, aggregated_data_path)
    aggregated_df = spark.read.parquet(aggregated_data_path)
    assert aggregated_df.count() == 5  # Ensure aggregation results are correct

    print("Full ETL pipeline test passed!")
