import pyspark.sql.functions as F

def clean_data(spark, input_path, output_path):
    """
    Cleans the input data by removing nulls and duplicates.
    """
    # Read data
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    # Perform cleaning
    clean_df = df.dropna().dropDuplicates()
    # Write cleaned data
    clean_df.coalesce(1).write.mode('overwrite').parquet(output_path)
    print(f"Data cleaning completed. Clean data saved to {output_path}")
