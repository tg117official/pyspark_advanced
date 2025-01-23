import pytest
from pyspark.sql import SparkSession
from src.data_cleaning import clean_data

@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.master("local").appName("test").getOrCreate()

def test_clean_data(spark, tmp_path):
    input_path = str(tmp_path / "input.csv")
    output_path = str(tmp_path / "output.parquet")
    schema_path = "resources/schema.json"

    # Create test data
    data = [("1", "John", "HR", 50000.0), (None, "Doe", "IT", 60000.0), ("1", "John", "HR", 50000.0)]
    columns = ["id", "name", "dept", "salary"]
    df = spark.createDataFrame(data, columns)
    df.write.csv(input_path, header=True, mode="overwrite")

    # Run cleaning function
    clean_data(spark, input_path, output_path, schema_path)

    # Validate results
    result_df = spark.read.parquet(output_path)
    assert result_df.count() == 1  # One valid row after cleaning
