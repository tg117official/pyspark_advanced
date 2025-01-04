def read_from_s3(spark, s3_path, file_format="csv", header=True, infer_schema=True):
    """
    Read a DataFrame from the specified S3 path.
    """
    return spark.read.format(file_format) \
        .option("header", header) \
        .option("inferSchema", infer_schema) \
        .load(s3_path)


def write_to_s3(df, s3_path, file_format="parquet", mode="overwrite"):
    """
    Write a DataFrame to the specified S3 path.
    """
    df.write.format(file_format).mode(mode).save(s3_path)
