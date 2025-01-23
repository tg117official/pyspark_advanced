import pytest
from pyspark.sql import SparkSession
from src.transformations import apply_transformations

@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.master("local").appName("test").getOrCreate()

def test_apply_transformations(spark, tmp_path):
    input_path = str(tmp_path / "input.parquet")
    output_path = str(tmp_path / "output.parquet")
    schema_path = "resources/schema.json"

    # Create test data
    data = [("HR", 50000.0), ("HR", 60000.0), ("IT", 70000.0)]
    columns = ["dept", "salary"]
    df = spark.createDataFrame(data, columns)
    df.write.mode("overwrite").parquet(input_path)

    # Run transformation
    apply_transformations(spark, input_path, output_path, schema_path)

    # Validate results
    result_df = spark.read.parquet(output_path)
    assert "salary_category" in result_df.columns
    assert result_df.where("dept = 'HR'").select("salary_category").distinct().count() == 2  # High and Low categories
