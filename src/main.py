# src/main.py

from config.config_loader import load_config
from data_ingestion.mqtt_client import start_mqtt_listener
from data_ingestion.http_client import fetch_http_data
from data_processing import start_stream_processing
from data_storage.db_handler import engine
from data_storage.schema import init_db
from fastapi import FastAPI
from .traffic_data import router as traffic_data_router
from .dependencies import get_db
from api.traffic_control import router as control_router

import threading

# Load the configuration from the YAML or .env file
config = load_config()

# Access specific config values, e.g. database URL or logging level
DATABASE_URL = config['database']['url']
LOG_LEVEL = config['logging']['level']

# Set up logging (example using logging level from config)
import logging
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

def main():
    # Start threads for each data source in the ingestion layer
    mqtt_thread = threading.Thread(target=start_mqtt_listener)
    http_thread = threading.Thread(target=fetch_http_data)

    # Start the data processing thread
    processing_thread = threading.Thread(target=start_stream_processing)

    # Start all threads
    mqtt_thread.start()
    http_thread.start()
    processing_thread.start()

    # Wait for all threads to complete
    mqtt_thread.join()
    http_thread.join()
    processing_thread.join()

if __name__ == "__main__":
    # Initialize database tables
    init_db(engine)
    # Start the rest of the application
    main()

app = FastAPI()

# Include the traffic data routes
app.include_router(traffic_data_router, prefix="/traffic_data", tags=["traffic_data"])

app.include_router(control_router, prefix="/control", tags=["control"])

# Optional: Include health check route
@app.get("/health")
def read_health():
    return {"status": "ok"}
