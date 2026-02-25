import yaml
import os

def load_execution_config(path=None):
    if path is None:
        # Resolve path relative to this file (core/yaml_reader.py -> ../yml/yl_execution.yml)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, "yml", "yl_execution.yml")

    with open(path, "r") as file:
        return yaml.safe_load(file)
