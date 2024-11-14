# src/data_processing/config.py
import os

AGGREGATION_INTERVAL = int(os.getenv("AGGREGATION_INTERVAL", 5))  # in seconds
CONGESTION_THRESHOLD = int(os.getenv("CONGESTION_THRESHOLD", 100))  # threshold for congestion
