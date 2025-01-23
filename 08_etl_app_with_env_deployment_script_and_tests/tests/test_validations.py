import pytest
from pyspark.sql import SparkSession
from src.validations import validate_dataframe

@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.master("local").appName("test").getOrCreate()

def test_validate_dataframe(spark, tmp_path):
    schema_path = tmp_path / "schema.json"
    schema_content = '{"fields": [{"name": "id", "type": "int", "nullable": false}]}'
    schema_path.write_text(schema_content)

    data = [(1,), (2,)]
    columns = ["id"]
    df = spark.createDataFrame(data, columns)

    result = validate_dataframe(df, str(schema_path))
    assert "Valid" in result  # Expecting validation success
