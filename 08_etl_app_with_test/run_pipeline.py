import yaml
from pyspark.sql import SparkSession
import pyspark.sql.functions as F


def read_config(config_path):
    """
    Reads configuration from a YAML file.
    """
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def clean_data(spark, input_path, output_path):
    """
    Cleans the input data by removing nulls and duplicates.
    """
    # Read data
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    # Perform cleaning
    clean_df = df.dropna().dropDuplicates()
    # Write cleaned data
    clean_df.coalesce(1).write.mode('overwrite').parquet(output_path)
    print(f"Data cleaning completed. Clean data saved to {output_path}")


def apply_transformations(spark, input_path, output_path):
    """
    Applies transformations to clean data.
    """
    # Read clean data
    df = spark.read.parquet(input_path)

    # Example transformation: Add a new column 'total_salary'
    avg_salary_per_dept = df.groupBy("dept").agg(F.avg("salary").alias("avg_salary"))
    transformed_data = df.join(avg_salary_per_dept, on="dept", how="inner") \
        .withColumn("salary_category", F.when(F.col("salary") > F.col("avg_salary"), "High").otherwise("Low"))

    # Write transformed data
    transformed_data.coalesce(1).write.mode('overwrite').parquet(output_path)
    print(f"Transformations completed. Transformed data saved to {output_path}")


def perform_aggregations(spark, input_path, output_path):
    """
    Performs aggregations on the transformed data.
    """
    # Read transformed data
    df = spark.read.parquet(input_path)

    # Example aggregation: Total sales by product
    aggregated_data = df.groupBy("dept").agg(
        F.sum("salary").alias("total_salary_expense"),
        F.count("id").alias("employee_count")
    )

    # Write aggregated data
    aggregated_data.write.mode('overwrite').parquet(output_path)
    print(f"Aggregations completed. Aggregated data saved to {output_path}")

def main():
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("Simple ETL App") \
        .getOrCreate()

    # Load configuration
    config = read_config(r"C:\Users\Sandeep\PycharmProjects\pyspark_advanced\02_etl_app_modules_copy\config\config.yaml")
    conf = config['paths']

    # Run ETL steps
    clean_data(spark, conf['input'], conf['clean_data'])

    # write_to_redshift(spark, conf['s3_output_path'], conf['redshift_jdbc_url'], conf['redshift_table'], conf['user'])
    apply_transformations(spark, conf['clean_data'], conf['transformed_data'])

    # Perform Aggregation on Final results
    perform_aggregations(spark, conf['transformed_data'], conf['aggregated_data'])

    spark.stop()

if __name__ == "__main__":
    main()
