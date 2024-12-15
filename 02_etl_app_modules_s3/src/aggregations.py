import pyspark.sql.functions as F

def perform_aggregations(spark, input_path, output_path):
    """
    Performs aggregations on the transformed data.
    """
    # Read transformed data
    df = spark.read.parquet(input_path)

    # Example aggregation: Total sales by product
    aggregated_df = df.groupBy("product_id").agg(
        F.sum("total_salary").alias("total_sales")
    )

    # Write aggregated data
    aggregated_df.write.mode('overwrite').parquet(output_path)
    print(f"Aggregations completed. Aggregated data saved to {output_path}")
