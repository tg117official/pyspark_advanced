import yaml
import logging
import json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

# Custom logger for utils module
logger = logging.getLogger("utils_logger")


def read_config(config_path):
    """
    Reads configuration from a YAML file.
    """
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file: {e}")
        raise


def load_schema(schema_path):
    """
    Loads schema from a JSON file and converts it to a PySpark StructType.
    """
    try:
        with open(schema_path, 'r') as file:
            schema_dict = json.load(file)

        # Convert schema to StructType
        struct_fields = []
        for field in schema_dict["fields"]:
            field_name = field["name"]
            field_type = field["type"].lower()
            nullable = field["nullable"]

            if field_type == "string":
                struct_fields.append(StructField(field_name, StringType(), nullable))
            elif field_type == "double":
                struct_fields.append(StructField(field_name, DoubleType(), nullable))
            elif field_type == "int":
                struct_fields.append(StructField(field_name, IntegerType(), nullable))
            else:
                raise ValueError(f"Unsupported field type: {field_type} in schema for field: {field_name}")

        schema = StructType(struct_fields)
        logger.info("Schema loaded and converted to StructType successfully.")
        return schema
    except FileNotFoundError as e:
        logger.error(f"Schema file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing schema JSON: {e}")
        raise
