import os
import pytest
import tempfile
import shutil
from pyspark.sql import SparkSession
import yaml
from run_pipeline import read_config, clean_data, apply_transformations, perform_aggregations
from pyspark.sql import Row

os.environ['PYSPARK_PYTHON']=r"C:\Users\Sandeep\PycharmProjects\pyspark_advanced\.venv\Scripts\python.exe"
os.environ['JAVA_HOME']=r'C:\Program Files\Java\jdk-1.8'
@pytest.fixture(scope="module")
def spark_session():
    """Creates a PySpark session for testing."""
    spark = SparkSession.builder \
        .appName("Test ETL App") \
        .master("local[2]") \
        .getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture
def temp_dir():
    """Creates a temporary directory for input/output data."""
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)

def test_read_config():
    """Tests the read_config function."""
    config_content = """
    paths:
        input: "data/input/employee_new.csv"
        clean_data: "data/output/clean_data"
        transformed_data: "data/output/final_data"
        aggregated_data: "data/output/aggregated_data"
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as tmp_file:
        tmp_file.write(config_content.encode())
        tmp_file.close()
        config = read_config(tmp_file.name)
        assert config["paths"]["input"] == "data/input/employee_new.csv"
        assert config["paths"]["clean_data"] == "data/output/clean_data"


from pyspark.sql import Row


def test_clean_data(spark_session, temp_dir):
    """Tests the clean_data function."""
    # Input data using Row objects
    input_data = [
        Row(id="1", name="John", salary=5000, dept="IT"),
        Row(id="2", name=None, salary=7000, dept="HR"),
        Row(id="3", name="Jane", salary=5000, dept="IT")
    ]

    # Create DataFrame without specifying schema explicitly
    df = spark_session.createDataFrame(input_data)

    # Save DataFrame as CSV for testing clean_data
    input_path = f"{temp_dir}/input.csv"
    df.write.csv(input_path, header=True, mode="overwrite")

    # Output path for cleaned data
    output_path = f"{temp_dir}/clean_data"

    # Call clean_data function
    clean_data(spark_session, input_path, output_path)

    # Validate output
    result_df = spark_session.read.parquet(output_path)
    assert result_df.count() == 2  # Only valid rows should remain
    assert "id" in result_df.columns  # Ensure all columns exist


def test_apply_transformations(spark_session, temp_dir):
    """Tests the apply_transformations function."""
    input_data = [Row(id="1", dept="IT", salary=5000),
                  Row(id="2", dept="HR", salary=7000),
                  Row(id="3", dept="IT", salary=6000)]
    input_path = f"{temp_dir}/clean_data"
    output_path = f"{temp_dir}/transformed_data"

    # Create test Parquet file
    df = spark_session.createDataFrame(input_data)
    df.write.parquet(input_path)

    # Run apply_transformations
    apply_transformations(spark_session, input_path, output_path)

    # Validate output
    result_df = spark_session.read.parquet(output_path)
    assert "salary_category" in result_df.columns

def test_perform_aggregations(spark_session, temp_dir):
    """Tests the perform_aggregations function."""
    input_data = [Row(id="1", dept="IT", salary=5000),
                  Row(id="2", dept="HR", salary=7000),
                  Row(id="3", dept="IT", salary=6000)]

    input_schema = ["id", "dept", "salary"]
    input_path = f"{temp_dir}/transformed_data"
    output_path = f"{temp_dir}/aggregated_data"

    # Create test Parquet file
    df = spark_session.createDataFrame(input_data)
    df.write.parquet(input_path)

    # Run perform_aggregations
    perform_aggregations(spark_session, input_path, output_path)

    # Validate output
    result_df = spark_session.read.parquet(output_path)
    assert "total_salary_expense" in result_df.columns
    assert "employee_count" in result_df.columns
    assert result_df.count() == 2  # Two departments aggregated

if __name__ == "__main__":
    pytest.main()
