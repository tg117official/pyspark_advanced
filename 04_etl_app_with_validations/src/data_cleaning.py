import logging
from src.validations import validate_dataframe
from pyspark.sql.utils import AnalysisException

logger = logging.getLogger("data_cleaning_logger")

def clean_data(spark, input_path, output_path, schema_path):
    """
    Cleans the input data by removing nulls and duplicates and validates schema.
    """
    try:
        # Read data
        df = spark.read.csv(input_path, header=True, inferSchema=True)
        logger.info(f"Data read from {input_path} successfully.")

        # Validate the raw DataFrame
        validate_dataframe(df, schema_path, logger)

        # Perform cleaning
        clean_df = df.dropna().dropDuplicates()
        logger.info("Data cleaned by dropping nulls and duplicates.")

        # Validate the cleaned DataFrame
        validate_dataframe(clean_df, schema_path, logger)

        # Write cleaned data
        clean_df.write.mode('overwrite').parquet(output_path)
        logger.info(f"Clean data written to {output_path} successfully.")
    except Exception as e:
        logger.error(f"Error during data cleaning: {e}")
        raise
