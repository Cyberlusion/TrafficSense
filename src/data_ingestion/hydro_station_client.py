# Ingest Data from Hydrometeorological Stations

# Many government agencies provide public APIs for weather data. 
# For example, if your area has an open data API, you could create a scheduled task to poll the API periodically.

# src/data_ingestion/hydro_station_client.py

import requests
import logging
from data_processing.stream_processor import process_and_store_weather_data

HYDRO_API_URL = "https://api.local_hydro_service.com/weather"

def fetch_hydro_data():
    try:
        response = requests.get(HYDRO_API_URL)
        if response.status_code == 200:
            hydro_data = response.json()
            logging.info(f"Received hydrometeorological data: {hydro_data}")
            process_and_store_weather_data(hydro_data)
        else:
            logging.error(f"Failed to fetch hydro data: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Error fetching hydro data: {e}")
