from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("RedshiftReadExample") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.457") \
    .getOrCreate()

# Redshift JDBC URL
redshift_jdbc_url = "jdbc:redshift:iam://redshift-cluster-1.csffclbtp7ut.us-east-2.redshift.amazonaws.com:5439/dev"

# IAM Role ARN
iam_role = "arn:aws:iam::146334643284:role/service-role/AmazonEMR-InstanceProfile-20240324T112710"

# Table and Query Options
redshift_table = "public.sales"
query = f"(SELECT * FROM {redshift_table}) AS sales_table"

# Read Data from Redshift
sales_df = spark.read \
    .format("jdbc") \
    .option("url", redshift_jdbc_url) \
    .option("query", query) \
    .option("aws_iam_role", iam_role) \
    .option("driver", "com.amazon.redshift.jdbc42.Driver") \
    .load()

# Show the Data
sales_df.show()

# Stop Spark Session
spark.stop()
