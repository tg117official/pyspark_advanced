from pyspark.sql import SparkSession
from src.data_cleaning import clean_data
from src.transformations import apply_transformations
from src.aggregations import perform_aggregations
from src.utils import read_config

def main():
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("Simple ETL App") \
        .getOrCreate()

    # Load configuration
    config = read_config("config/config.yaml")
    paths = config['paths']

    # Run ETL steps
    clean_data(spark, paths['input'], paths['clean_data'])
    apply_transformations(spark, paths['clean_data'], paths['transformed_data'])

    spark.stop()

if __name__ == "__main__":
    main()
