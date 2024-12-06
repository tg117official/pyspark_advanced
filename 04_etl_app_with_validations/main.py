import logging
import logging.config
import yaml
from pyspark.sql import SparkSession
from src.data_cleaning import clean_data
from src.transformations import apply_transformations
from src.aggregations import perform_aggregations
from src.utils import read_config, load_schema

# Load logging configuration
with open("config/logging_config.yaml", "r") as f:
    logging.config.dictConfig(yaml.safe_load(f))

# Custom logger for main script
logger = logging.getLogger("main_logger")

def main():
    try:
        # Initialize SparkSession
        spark = SparkSession.builder \
            .appName("Robust ETL App") \
            .getOrCreate()
        logger.info("SparkSession initialized successfully.")

        # Load configuration
        config = read_config("config/config.yaml")
        paths = config['paths']

        # Load schema
        schema = load_schema("resources/schema.json")
        logger.info(f"Schema loaded successfully. : {schema}")

        # Run ETL steps
        clean_data(spark, paths['input'], paths['clean_data'], schema)
        apply_transformations(spark, paths['clean_data'], paths['transformed_data'])
        perform_aggregations(spark, paths['transformed_data'], paths['aggregated_data'])

    except Exception as e:
        logger.critical(f"Critical error in ETL process: {e}")
    finally:
        spark.stop()
        logger.info("SparkSession stopped. ETL process completed.")

if __name__ == "__main__":
    main()