from pyspark.sql import SparkSession

# Function to initialize the Spark session with configurations
def initialize_spark(app_name):
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()

# Function to read a DataFrame from S3
def read_from_s3(spark, s3_path, file_format="csv", header=True, infer_schema=True):
    df = spark.read.format(file_format) \
        .option("header", header) \
        .option("inferSchema", infer_schema) \
        .load(s3_path)
    return df

# Function to clean the DataFrame (remove duplicates)
def clean_dataframe(df):
    return df.dropDuplicates()

# Function to write a DataFrame to S3
def write_to_s3(df, s3_path, file_format="parquet", mode="overwrite"):
    df.write.format(file_format).mode(mode).save(s3_path)

if __name__ == "__main__":
    # Configurations
    config = {
        "app_name": "PySpark S3 Example",
        "s3_source_path": "s3://emr-serverless-tg117/data/input/employee_new.csv",
        "s3_destination_path": "s3://emr-serverless-tg117/data/output/clean_data/",
        "input_format": "csv",
        "output_format": "parquet",
        "write_mode": "overwrite",
        "header": True,
        "infer_schema": True
    }

    # Initialize Spark session
    spark = initialize_spark(config["app_name"])

    # Step 1: Read the DataFrame from S3
    source_df = read_from_s3(spark, config["s3_source_path"], config["input_format"], config["header"], config["infer_schema"])

    # Step 2: Clean the DataFrame
    cleaned_df = clean_dataframe(source_df)

    # Step 3: Write the cleaned DataFrame to S3
    write_to_s3(cleaned_df, config["s3_destination_path"], config["output_format"], config["write_mode"])

    # Stop the Spark session
    spark.stop()


