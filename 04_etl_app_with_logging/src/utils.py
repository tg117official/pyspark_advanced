import yaml
import logging

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
