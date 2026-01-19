"""
Configuration utilities for the Dynatrace network agent.

Provides helpers to resolve resource paths (PyInstaller/dev) and to load settings from config.yaml.
"""
import os
import sys
import yaml

def resource_path(relative_path: str) -> str:
    """
    Resolve path for PyInstaller (--onefile) and dev mode
    """
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))  # PyInstaller temp dir

    return os.path.join(base_path, relative_path)

def load_config() -> dict:
    """
    Load configuration from config.yaml and return it as a dictionary.
    """
    config_file = resource_path("config.yaml")
    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)