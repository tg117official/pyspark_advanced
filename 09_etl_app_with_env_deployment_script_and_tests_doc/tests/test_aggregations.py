import pytest
from pyspark.sql import SparkSession
from src.aggregations import perform_aggregations

@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.master("local").appName("test").getOrCreate()

def test_perform_aggregations(spark, tmp_path):
    input_path = str(tmp_path / "input.parquet")
    output_path = str(tmp_path / "output.parquet")

    # Create test data
    data = [("P1", 100.0), ("P1", 200.0), ("P2", 300.0)]
    columns = ["product_id", "total_salary"]
    df = spark.createDataFrame(data, columns)
    df.write.mode("overwrite").parquet(input_path)

    # Run aggregation
    perform_aggregations(spark, input_path, output_path)

    # Validate results
    result_df = spark.read.parquet(output_path)
    assert result_df.count() == 2
    assert result_df.where("product_id = 'P1'").select("total_sales").collect()[0][0] == 300.0
