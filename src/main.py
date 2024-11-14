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
from data_ingestion.loop_sensor_client import start_loop_sensor_listener
from data_ingestion.radar_lidar_client import start_radar_lidar_listener

import threading import Thread

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

if __name__ == "__main__":
    # Initialize database tables
    init_db(engine)
    # Start the rest of the application
    main()

app = FastAPI()

# Optional: Include health check route
@app.get("/health")
def read_health():
    return {"status": "ok"}

# Integrate Traffic Camera Data in the Main Application

from threading import Thread
from data_ingestion.traffic_camera_client import start_camera_stream
from data_ingestion.mqtt_client import start_mqtt_listener
from data_ingestion.http_client import fetch_http_data
from data_processing import start_stream_processing

CAMERA_URL = "rtsp://camera_address/stream"  # Replace with actual camera URL

CAMERA_URL = "rtsp://camera_address/stream"  # Replace with actual camera URL

if __name__ == "__main__":
    
    # Start threads for each data source
    mqtt_thread = Thread(target=start_mqtt_listener)
    http_thread = Thread(target=fetch_http_data)
    camera_thread = Thread(target=start_camera_stream, args=(CAMERA_URL,))
    loop_sensor_thread = Thread(target=start_loop_sensor_listener)
    radar_lidar_thread = Thread(target=start_radar_lidar_listener)
    processing_thread = Thread(target=start_stream_processing)

    # Start all threads
    mqtt_thread.start()
    http_thread.start()
    camera_thread.start()
    loop_sensor_thread.start()
    radar_lidar_thread.start()
    processing_thread.start()

    # Wait for all threads to complete
    mqtt_thread.join()
    http_thread.join()
    camera_thread.join()
    loop_sensor_thread.join()
    radar_lidar_thread.join()
    processing_thread.join()
