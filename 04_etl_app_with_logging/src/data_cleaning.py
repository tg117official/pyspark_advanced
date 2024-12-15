import logging
import pyspark.sql.functions as F

# Custom logger for data_cleaning module
logger = logging.getLogger("data_cleaning_logger")

def clean_data(spark, input_path, output_path):
    """
    Cleans the input data by removing nulls and duplicates.
    """
    try:
        # Read data
        df = spark.read.csv(input_path, header=True, inferSchema=True)
        logger.info(f"Data read from {input_path} successfully.")

        # Perform cleaning
        clean_df = df.dropna().dropDuplicates()
        logger.info("Data cleaned by dropping nulls and duplicates.")

        # Write cleaned data
        clean_df.coalesce(1).write.mode('overwrite').parquet(output_path)
        logger.info(f"Clean data written to {output_path} successfully.")
    except Exception as e:
        logger.error(f"Error during data cleaning: {e}")
        raise
