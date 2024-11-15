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
from data_ingestion.acoustic_sensor_client import start_acoustic_listener
from data_ingestion.air_quality_sensor_client import start_air_quality_listener
from data_ingestion.gps_client import start_gps_listener
from data_ingestion.weather_sensor_client import start_weather_listener
from data_ingestion.hydro_station_client import fetch_hydro_data
from data_ingestion.pedestrian_counter_client import start_pedestrian_listener

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

if __name__ == "__main__":
    # Start threads for each data source
    bluetooth_thread = Thread(target=start_bluetooth_listener)
    wifi_thread = Thread(target=start_wifi_listener)
    gps_thread = Thread(target=start_gps_listener)
    mqtt_thread = Thread(target=start_mqtt_listener)
    http_thread = Thread(target=fetch_http_data)
    camera_thread = Thread(target=start_camera_stream, args=("camera_url",))
    loop_sensor_thread = Thread(target=start_loop_sensor_listener)
    radar_lidar_thread = Thread(target=start_radar_lidar_listener)
    air_quality_thread = Thread(target=start_air_quality_listener)
    processing_thread = Thread(target=start_stream_processing)
    weather_thread = Thread(target=start_weather_listener)
    hydro_data_thread = Thread(target=fetch_hydro_data)
    pedestrian_thread = Thread(target=start_pedestrian_listener)

    # Start all threads
    bluetooth_thread.start()
    wifi_thread.start()
    gps_thread.start()
    mqtt_thread.start()
    http_thread.start()
    camera_thread.start()
    loop_sensor_thread.start()
    radar_lidar_thread.start()
    air_quality_thread.start()
    processing_thread.start()
    weather_thread.start()
    hydro_data_thread.start()
    pedestrian_thread.start()

    # Wait for all threads to complete
    bluetooth_thread.join()
    wifi_thread.join()
    gps_thread.join()
    mqtt_thread.join()
    http_thread.join()
    camera_thread.join()
    loop_sensor_thread.join()
    radar_lidar_thread.join()
    air_quality_thread.join()
    processing_thread.join()
    weather_thread.join()
    hydro_data_thread.join()
    pedestrian_thread.join()
