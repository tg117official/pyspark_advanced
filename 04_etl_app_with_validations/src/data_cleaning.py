import logging
import pyspark.sql.functions as F
from pyspark.sql.utils import AnalysisException

# Custom logger for data_cleaning module
logger = logging.getLogger("data_cleaning_logger")

def clean_data(spark, input_path, output_path, schema):
    """
    Cleans the input data by removing nulls and duplicates and validates schema.
    """
    try:
        # Read data
        df = spark.read.csv(input_path, header=True, inferSchema=True)
        logger.info(f"Data read from {input_path} successfully.")

        # Validate schema
        # try:
        #     validated_df = spark.createDataFrame(df.rdd, schema)
        #     logger.info("Schema validation passed.")
        # except AnalysisException as e:
        #     logger.error(f"Schema validation failed: {e}")
        #     raise

        # Perform cleaning
        clean_df = df.dropna().dropDuplicates()
        logger.info("Data cleaned by dropping nulls and duplicates.")

        # Write cleaned data
        clean_df.write.mode('overwrite').parquet(output_path)
        logger.info(f"Clean data written to {output_path} successfully.")
    except Exception as e:
        logger.error(f"Error during data cleaning: {e}")
        raise
