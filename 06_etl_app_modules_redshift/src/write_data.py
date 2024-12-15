

def write_to_redshift(spark, clean_data , conn_str, table, user) :
    # Read data from S3
    df = spark.read.csv(clean_data, header=True, inferSchema=True)

    # Show data (optional, for debugging)
    df.show()

    # Write data to Redshift
    df.write \
        .format("jdbc") \
        .option("url", conn_str) \
        .option("dbtable", table) \
        .option("user", user) \
        .option("driver", "com.amazon.redshift.jdbc42.Driver") \
        .mode("overwrite") \
        .save()

    print("Data written successfully to Redshift using IAM Role.")