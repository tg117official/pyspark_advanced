import pyspark.sql.functions as F

def apply_transformations(spark, input_path, output_path):
    """
    Applies transformations to clean data.
    """
    # Read clean data
    df = spark.read.parquet(input_path)

    # Example transformation: Add a new column 'total_salary'
    avg_salary_per_dept = df.groupBy("dept").agg(F.avg("salary").alias("avg_salary"))
    transformed_data = df.join(avg_salary_per_dept, on="dept", how="inner") \
        .withColumn("salary_category", F.when(F.col("salary") > F.col("avg_salary"), "High").otherwise("Low"))

    # Write transformed data
    transformed_data.coalesce(1).write.mode('overwrite').parquet(output_path)
    print(f"Transformations completed. Transformed data saved to {output_path}")
