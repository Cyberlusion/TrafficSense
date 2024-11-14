#Set Up GPS Data Ingestion

#GPS data is often transmitted in JSON format via HTTP, MQTT, or other protocols. 
#For this example, we'll assume the data comes in via MQTT, with attributes like vehicle ID, latitude, longitude, speed, and timestamp.

import json
import logging
import paho.mqtt.client as mqtt
from data_processing.stream_processor import process_and_store_gps_data

def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode("utf-8"))
    vehicle_id = payload.get("vehicle_id")
    latitude = payload.get("latitude")
    longitude = payload.get("longitude")
    speed = payload.get("speed")
    timestamp = payload.get("timestamp")

    if vehicle_id and latitude and longitude and speed and timestamp:
        logging.info(f"Received GPS data for Vehicle ID {vehicle_id}: Lat={latitude}, Long={longitude}, Speed={speed}, Timestamp={timestamp}")
        process_and_store_gps_data(vehicle_id, latitude, longitude, speed, timestamp)

def start_gps_listener():
    client = mqtt.Client("GPSListener")
    client.connect("localhost", 1883)  # MQTT broker address and port
    client.subscribe("traffic/gps")
    client.on_message = on_message

    client.loop_start()
