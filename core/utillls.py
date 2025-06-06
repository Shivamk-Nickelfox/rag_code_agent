# utils.py

import os
import yaml

def is_ignored_file(file_path, ignore_list):
    return any(ignored in file_path for ignored in ignore_list)

def read_file_safely(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None

def load_config(path='config/settings.yaml'):
    """Load YAML config file."""
    with open(path, 'r') as f:
        return yaml.safe_load(f)
     