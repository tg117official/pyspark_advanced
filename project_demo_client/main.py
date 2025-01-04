
# import sys
# sys.path.insert(0, "project/src")
import boto3
import yaml
from src.spark_utils import initialize_spark
from src.s3_operations import read_from_s3, write_to_s3
from src.data_cleaning import clean_dataframe

def load_config():
    """
    Load configuration from a YAML file.
    """
    s3_uri = "s3://emr-serverless-tg117/scripts/config.yaml"

    s3_uri_parts = s3_uri[5:].split("/", 1)
    bucket_name = s3_uri_parts[0]
    file_key = s3_uri_parts[1]

    s3 = boto3.client('s3')

    # Download the file content from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_content = response['Body'].read().decode('utf-8')

    # Parse YAML content
    config = yaml.safe_load(file_content)

    return config

if __name__ == "__main__":
    # Load configurations
    config = load_config()

    # Step 1: Initialize Spark session
    spark = initialize_spark(config["app_name"])

    # Step 2: Read the DataFrame from S3
    source_df = read_from_s3(
        spark,
        config["s3_source_path"],
        config["input_format"],
        config["header"],
        config["infer_schema"]
    )

    # Step 3: Clean the DataFrame
    cleaned_df = clean_dataframe(source_df)

    # Step 4: Write the cleaned DataFrame to S3
    write_to_s3(
        cleaned_df,
        config["s3_destination_path"],
        config["output_format"],
        config["write_mode"]
    )

    # Stop the Spark session
    spark.stop()
