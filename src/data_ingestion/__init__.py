# src/data_ingestion/__init__.py

from .mqtt_client import start_mqtt_listener
from .http_client import fetch_http_data
from .kafka_producer import produce_to_kafka

# src/data_ingestion/__init__.py

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Data ingestion package initialized")
