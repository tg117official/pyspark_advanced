import yaml
import boto3
from src.spark_utils import initialize_spark
from src.s3_operations import read_from_s3, write_to_s3
from src.data_cleaning import clean_dataframe
from urllib.parse import urlparse

def load_config(config_file: str):
    """
    Load configuration from a YAML file.
    Supports both local file paths and S3 paths (s3://bucket/key).
    """
    if config_file.startswith("s3://"):
        # Parse bucket and key from S3 path
        parsed = urlparse(config_file)
        bucket = parsed.netloc
        key = parsed.path.lstrip("/")

        print(bucket, key)

        # Read from S3
        s3 = boto3.client("s3")
        obj = s3.get_object(Bucket=bucket, Key=key)
        content = obj["Body"].read().decode("utf-8")

        return yaml.safe_load(content)
    else:
        # Fallback to local file
        with open(config_file, "r") as file:
            return yaml.safe_load(file)


if __name__ == "__main__":
    # Load configurations
    config = load_config("s3://emr-exercises-tg117/config/config.yaml")

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
