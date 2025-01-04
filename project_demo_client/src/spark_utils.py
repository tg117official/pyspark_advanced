from pyspark.sql import SparkSession

def initialize_spark(app_name):
    """
    Initialize the Spark session with the specified application name.
    """
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()
