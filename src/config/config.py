#This file holds the default or general configurations for the application that can be shared across environments (like logging configuration, database connections, etc.).

# src/config/config.py

import os

class Config:
    """Base configuration class with default settings."""
    PROJECT_NAME = "Traffic Data Processing"
    LOG_LEVEL = "INFO"  # Default log level
    DATABASE_URL = "sqlite:///./test.db"  # Default database URL (can be overwritten by specific environments)
    API_KEY = os.getenv("API_KEY", "default-api-key")  # Retrieve API Key from environment variable if set
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration class."""
    DATABASE_URL = "postgresql://dev_user:dev_pass@localhost/dev_db"
    DEBUG = True
    LOG_LEVEL = "DEBUG"

class ProductionConfig(Config):
    """Production configuration class."""
    DATABASE_URL = "postgresql://prod_user:prod_pass@prod_host/prod_db"
    DEBUG = False
    LOG_LEVEL = "ERROR"

class TestingConfig(Config):
    """Testing configuration class."""
    DATABASE_URL = "postgresql://test_user:test_pass@localhost/test_db"
    TESTING = True
    LOG_LEVEL = "WARNING"
