import yaml

def read_config(config_path):
    """
    Reads configuration from a YAML file.
    """
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)
