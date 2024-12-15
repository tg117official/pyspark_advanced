# Initialize Spark session
from pyspark.sql import SparkSession

# Define the paths to the JARs
jars = r"C:\Users\Sandeep\PycharmProjects\pyspark_advanced\.venv\Lib\site-packages\pyspark\jars\jackson-databind-2.15.0.jar," \
       r"C:\Users\Sandeep\PycharmProjects\pyspark_advanced\.venv\Lib\site-packages\pyspark\jars\jackson-core-2.15.0.jar," \
       r"C:\Users\Sandeep\PycharmProjects\pyspark_advanced\.venv\Lib\site-packages\pyspark\jars\jackson-annotations-2.15.0.jar,"\
       r"C:\Users\Sandeep\PycharmProjects\pyspark_advanced\.venv\Lib\site-packages\pyspark\jars\redshift-jdbc42-2.1.0.31.jar" \


# Initialize the Spark session with JARs
spark = SparkSession.builder \
    .appName("MySparkApplication") \
    .config("spark.jars", jars) \
    .getOrCreate()


# spark = SparkSession.builder \
#     .appName("ReadFromRedshift") \
#     .config("spark.driver.extraClassPath", r"C:\Users\Sandeep\PycharmProjects\pyspark_advanced\.venv\Lib\site-packages\pyspark\jars\redshift-jdbc42-2.1.0.31.jar") \
#     .getOrCreate()


# Redshift connection details
redshift_url = "jdbc:redshift://demo-cluster.cw38oxiq9pss.ap-southeast-2.redshift.amazonaws.com:5439/dev"
redshift_properties = {
    "user": "awsuser",
    "password": "Admin_awsuser01",
    "driver": "com.amazon.redshift.jdbc42.Driver"
}

# Query the Redshift table
df = spark.read \
    .format("jdbc") \
    .option("url", redshift_url) \
    .option("dbtable", "public.sales") \
    .options(**redshift_properties) \
    .load()

df.show()
