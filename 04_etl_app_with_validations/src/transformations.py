import logging
import pyspark.sql.functions as F
from src.validations import validate_dataframe

logger = logging.getLogger("transformations_logger")

def apply_transformations(spark, input_path, output_path, schema_path):
    """
    Applies transformations to clean data.
    """
    try:
        # Read clean data
        df = spark.read.parquet(input_path)
        logger.info(f"Clean data read from {input_path} successfully.")

        # Validate the input DataFrame
        validate_dataframe(df, schema_path, logger)

        # Example transformation: Add a new column 'total_salary'
        avg_salary_per_dept = df.groupBy("dept").agg(F.avg("salary").alias("avg_salary"))
        transformed_data = df.join(avg_salary_per_dept, on="dept", how="inner") \
            .withColumn("salary_category", F.when(F.col("salary") > F.col("avg_salary"), "High").otherwise("Low"))

        # Validate the transformed DataFrame
        validate_dataframe(transformed_data, schema_path, logger)

        # Write transformed data
        transformed_data.coalesce(1).write.mode('overwrite').parquet(output_path)
        logger.info("Transformation applied and data written successfully.")
    except Exception as e:
        logger.error(f"Error during data transformations: {e}")
        raise
