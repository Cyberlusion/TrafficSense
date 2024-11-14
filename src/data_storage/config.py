# src/data_storage/config.py
#Define configuration variables for your database connection (like credentials, database URL, or connection parameters) to keep them organized and separate from your main logic.

import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))  # Default PostgreSQL port
DB_NAME = os.getenv("DB_NAME", "traffic_data")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
