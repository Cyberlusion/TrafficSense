#Load Configuration Based on Environment

#This file contains logic for loading the correct configuration depending on the environment. 
#It can use environment variables or command-line arguments to choose between development, production, or testing settings.

# src/config/config_loader.py

import os
from .config import DevelopmentConfig, ProductionConfig, TestingConfig

def get_config():
    """Return the appropriate configuration class based on the environment variable."""
    env = os.getenv("APP_ENV", "development").lower()
    
    if env == "production":
        return ProductionConfig
    elif env == "testing":
        return TestingConfig
    else:
        return DevelopmentConfig
