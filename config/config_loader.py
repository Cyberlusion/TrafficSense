#To load configuration from YAML or JSON, you might create a utility that reads the file and loads the values into the application.

import yaml
import json
import os

def load_config(config_file='config/config.yaml'):
    """Loads the configuration file (YAML or JSON) into a Python dictionary."""
    file_extension = os.path.splitext(config_file)[1].lower()

    if file_extension == '.yaml' or file_extension == '.yml':
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
    elif file_extension == '.json':
        with open(config_file, 'r') as file:
            config = json.load(file)
    else:
        raise ValueError("Unsupported config file format: should be .yaml, .yml, or .json")
    
    return config
