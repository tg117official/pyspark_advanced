import logging
import logging.config
import yaml
import argparse
from pyspark.sql import SparkSession
from src.data_cleaning import clean_data
from src.transformations import apply_transformations
from src.aggregations import perform_aggregations
from src.utils import load_schema



# Parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="ETL pipeline for dev/prod environments.")
    parser.add_argument("--env", required=True, choices=["dev", "prod"], help="Specify the environment (dev or prod).")
    return parser.parse_args()


# Load environment-specific configuration
def load_environment_config(env):
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config["environments"].get(env)


# Load logging configuration
def setup_logging():
    with open("config/logging_config.yaml", "r") as f:
        logging_config = yaml.safe_load(f)
        logging.config.dictConfig(logging_config)


def main():
    # Set up logging
    setup_logging()
    logger = logging.getLogger("main_logger")

    # Parse command-line arguments
    args = parse_arguments()
    env = args.env

    # Load environment-specific configuration
    config = load_environment_config(env)
    if not config:
        logger.critical(f"Invalid environment: {env}")
        raise ValueError(f"Invalid environment: {env}")

    paths = config["paths"]
    logging_level = config["logging_level"]

    logger.info(f"Starting ETL pipeline in {env} environment.")
    try:
        # Initialize SparkSession
        spark = SparkSession.builder \
            .appName("Robust ETL App") \
            .getOrCreate()
        logger.info(f"SparkSession initialized successfully for {env} environment.")

        # Load schema
        schema = load_schema("resources/schema.json")
        logger.info(f"Schema loaded successfully: {schema}")

        # Run ETL steps
        logger.info("Starting data cleaning step.")
        clean_data(spark, paths["input"], paths["clean_data"], schema)
        logger.info("Data cleaning completed.")

        logger.info("Starting transformations step.")
        apply_transformations(spark, paths["clean_data"], paths["transformed_data"], schema)
        logger.info("Transformations completed.")

        logger.info("Starting aggregations step.")
        perform_aggregations(spark, paths["transformed_data"], paths["aggregated_data"])
        logger.info("Aggregations completed.")

    except Exception as e:
        logger.critical(f"Critical error in ETL process: {e}")
        raise
    finally:
        spark.stop()
        logger.info(f"SparkSession stopped. ETL process for {env} environment completed.")


if __name__ == "__main__":
    main()
