import yaml
from pyspark.sql import SparkSession
from src.reader import read_data
from src.writer import write_data

def load_config(config_path: str) -> dict:
    """
    Loads configuration from a YAML file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Configuration dictionary.
    """
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def main():
    # Load configuration
    config_path = "config/config.yaml"
    config = load_config(config_path)

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName(config["app_name"]) \
        .getOrCreate()

    # Read data
    df = read_data(spark, config)

    # Perform any transformation (if needed) - Example: Simple transformation
    clean_df = df.dropna()  # Drop rows with null values

    # Write data
    write_data(clean_df, config)

    # Stop Spark session
    spark.stop()

if __name__ == "__main__":
    main()
