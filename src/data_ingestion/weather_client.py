#Ingest data from IoT-based weather sensors using protocols like MQTT for lightweight communication, HTTP for simple REST APIs, or BLE for low-energy Bluetooth-based devices.

#Example for MQTT-based weather sensors:

# src/data_ingestion/weather_sensor_client.py

import json
import logging
from mqtt_client import mqtt_client
from data_processing.stream_processor import process_and_store_weather_data

def start_weather_listener():
    def on_message(client, userdata, message):
        try:
            weather_data = json.loads(message.payload.decode())
            logging.info(f"Received weather data: {weather_data}")
            process_and_store_weather_data(weather_data)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding weather data: {e}")

    mqtt_client.subscribe("weather/sensors")
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()
