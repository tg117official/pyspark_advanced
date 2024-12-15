from pyspark.sql import SparkSession

# Define input and output details
s3_input_path = "s3://emr-serverless-tg117/data/input/employee_new.csv"
redshift_jdbc_url = "jdbc:redshift:iam://redshift-cluster-1.csffclbtp7ut.us-east-2.redshift.amazonaws.com:5439/dev"
redshift_table = "public.employee"

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("S3 to Redshift with IAM Role") \
    .config("spark.jars.packages", "com.amazon.redshift:redshift-jdbc42:2.1.0,org.apache.hadoop:hadoop-aws:3.2.0") \
    .getOrCreate()

# Read data from S3
df = spark.read.csv(s3_input_path, header=True, inferSchema=True)

# Show data (optional, for debugging)
df.show()

# Write data to Redshift
df.write \
    .format("jdbc") \
    .option("url", redshift_jdbc_url) \
    .option("dbtable", redshift_table) \
    .option("user", "iam_user") \
    .option("driver", "com.amazon.redshift.jdbc42.Driver") \
    .mode("overwrite") \
    .save()

print("Data written successfully to Redshift using IAM Role.")

# Stop Spark session
spark.stop()
