# import pandas as pd
from pyspark.sql import SparkSession

# Define the paths to the JARs
jars = r"C:\Users\Sandeep\PycharmProjects\pyspark_advanced\.venv\Lib\site-packages\pyspark\jars\jackson-databind-2.15.0.jar," \
       r"C:\Users\Sandeep\PycharmProjects\pyspark_advanced\.venv\Lib\site-packages\pyspark\jars\jackson-core-2.15.0.jar," \
       r"C:\Users\Sandeep\PycharmProjects\pyspark_advanced\.venv\Lib\site-packages\pyspark\jars\jackson-annotations-2.15.0.jar," \
       r"C:\Users\Sandeep\PycharmProjects\pyspark_advanced\.venv\Lib\site-packages\pyspark\jars\redshift-jdbc42-2.1.0.31.jar"

# Initialize Spark session
spark = SparkSession.builder \
    .appName("WriteToRedshift") \
    .config("spark.jars", jars) \
    .getOrCreate()

# Load the CSV file into a DataFrame
csv_file_path = r"C:\Users\Sandeep\PycharmProjects\pyspark_advanced\02_writing_data_to_destinations\data\employee_new.csv"  # Path to your CSV file
employee_df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(csv_file_path)

# Show the loaded data
print("Loaded data from CSV:")
employee_df.show()

# Redshift connection details
redshift_url = "jdbc:redshift://demo-cluster.cw38oxiq9pss.ap-southeast-2.redshift.amazonaws.com:5439/dev"
redshift_properties = {
    "user": "awsuser",
    "password": "Admin_awsuser01",
    "driver": "com.amazon.redshift.jdbc42.Driver"
}

# Write the DataFrame to the Redshift table
employee_df.write \
    .format("jdbc") \
    .option("url", redshift_url) \
    .option("dbtable", "public.employee") \
    .option("user", redshift_properties["user"]) \
    .option("password", redshift_properties["password"]) \
    .option("driver", redshift_properties["driver"]) \
    .mode("overwrite") \
    .save()

print("Data written to Redshift table public.employee successfully.")

# The isolation level requested by Spark (level 1: READ_UNCOMMITTED) is not supported by the
# Redshift JDBC driver.
# Redshift defaults to READ_COMMITTED (isolation level 8).
# This is a benign warning and doesn't affect the success of the operation in your case,
# as Redshift successfully wrote the data.


