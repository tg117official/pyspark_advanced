from pyspark import StorageLevel
from pyspark.sql import SparkSession
from src.data_cleaning import clean_data
from src.write_data import write_to_redshift
from src.utils import read_config

def main():
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("Simple ETL App") \
        .getOrCreate()
    # spark.sparkContext.addPyFile("s3://emr-serverless-tg117/scripts/etl_app_modules_code.zip")
    # Load configuration
    config = read_config("s3://emr-serverless-tg117/scripts/config.yaml")
    conf = config['paths']

    df = spark.range(1000)
    df.persist(StorageLevel())

    # Run ETL steps
    clean_data(spark, conf['s3_input_path'], conf['s3_output_path'])
    write_to_redshift(spark, conf['s3_output_path'], conf['redshift_jdbc_url'], conf['redshift_table'], conf['user'])

    spark.stop()

if __name__ == "__main__":
    main()
