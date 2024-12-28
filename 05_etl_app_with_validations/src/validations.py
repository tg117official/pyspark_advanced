import logging
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

logger = logging.getLogger('validations_logger')

def load_schema(schema_path):
    """Load schema from the provided JSON file."""
    with open(schema_path, 'r') as f:
        schema_json = json.load(f)
    fields = []
    for field in schema_json['fields']:
        field_type = {
            'int': IntegerType(),
            'string': StringType(),
            'double': DoubleType()
        }.get(field['type'])
        if field_type:
            fields.append(StructField(field['name'], field_type, field['nullable']))
    return StructType(fields)


def validate_dataframe(dataframe, schema_path, logger):
    """Validate the DataFrame against the schema and log results."""
    try :
        # Load schema from the JSON file
        with open(schema_path, 'r') as f:
            schema_json = json.load(f)
        fields = []
        for field in schema_json['fields']:
            field_type = {
                'int': IntegerType(),
                'string': StringType(),
                'double': DoubleType()
            }.get(field['type'])
            if field_type:
                fields.append(StructField(field['name'], field_type, field['nullable']))

        expected_schema = StructType(fields)

        # Print the first 5 rows of the DataFrame
        print("First 5 rows of the DataFrame:")
        dataframe.take(5)

        # Print and validate the schema
        print("Schema of the DataFrame:")
        dataframe.printSchema()

        # Compare with the expected schema
        is_schema_valid = dataframe.schema == expected_schema
        print(f"Schema validation result: {'Valid' if is_schema_valid else 'Invalid'}")

        # Log the results if logger is provided

        logger.info("First 5 rows of the DataFrame:")
        logger.info(dataframe.limit(5).collect())
        logger.info("Schema of the DataFrame:")
        logger.info(dataframe.schema.json())
        logger.info(f"Schema validation result: {'Valid' if is_schema_valid else 'Invalid'}")
    except Exception as e :
        return f"Error Occured During Validation : {e}"
        raise

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("DataFrame Validation") \
        .getOrCreate()

    data = [(1, "John", "Doe", "john.doe@example.com", "HR", 50000.0),
            (2, "Jane", "Smith", "jane.smith@example.com", "IT", 60000.0)]
    columns = ["id", "first_name", "last_name", "email", "dept", "salary"]
    example_df = spark.createDataFrame(data, columns)

    schema_path = "../resources/schema.json"
    validate_dataframe(example_df, schema_path)
