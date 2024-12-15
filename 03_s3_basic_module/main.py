from pyspark.sql import SparkSession
from data_ingest.data_ingestion import create_dataframe

def main():
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("S3 DataFrame Example") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.2") \
        .getOrCreate()

    # S3 file path
    file_path = "s3a://your-bucket-name/path/to/your-file.csv"

    # Options for CSV file
    options = {
        "header": "true",
        "inferSchema": "true"
    }

    # Create DataFrame
    df = create_dataframe(spark, file_path, format="csv", options=options)

    # Show DataFrame
    df.show()

    # Stop SparkSession
    spark.stop()

if __name__ == "__main__":
    main()
