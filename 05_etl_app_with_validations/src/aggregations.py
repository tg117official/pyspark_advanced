import logging
import pyspark.sql.functions as F

# Custom logger for aggregations module
logger = logging.getLogger("aggregations_logger")

def perform_aggregations(spark, input_path, output_path):
    """
    Performs aggregations on the transformed data.
    """
    try:
        # Read transformed data
        df = spark.read.parquet(input_path)
        logger.info(f"Transformed data read from {input_path} successfully.")

        # Example aggregation: Total sales by product
        aggregated_df = df.groupBy("product_id").agg(
            F.sum("total_salary").alias("total_sales")
        )
        logger.info("Aggregation applied: Total sales by product calculated.")

        # Write aggregated data
        aggregated_df.write.mode('overwrite').parquet(output_path)
        logger.info(f"Aggregated data written to {output_path} successfully.")
    except Exception as e:
        logger.error(f"Error during data aggregations: {e}")
        raise
