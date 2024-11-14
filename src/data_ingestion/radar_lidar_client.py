# Set Up Radar and Lidar Sensor Data Ingestion

# Assume that both radar and lidar sensors send data via MQTT with vehicle speed, distance, and object type.

import json
import logging
import paho.mqtt.client as mqtt
from data_processing.stream_processor import process_and_store_radar_lidar_data

def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode("utf-8"))
    sensor_type = payload.get("sensor_type")  # Either "radar" or "lidar"
    vehicle_data = payload.get("vehicle_data")  # List of vehicles detected by the sensor
    timestamp = payload.get("timestamp")

    if sensor_type and vehicle_data and timestamp:
        logging.info(f"Received data from {sensor_type} sensor: {vehicle_data}")
        process_and_store_radar_lidar_data(sensor_type, vehicle_data, timestamp)

def start_radar_lidar_listener():
    client = mqtt.Client("RadarLidarListener")
    client.connect("localhost", 1883)  # MQTT broker address and port
    client.subscribe("traffic/radar_lidar")
    client.on_message = on_message

    client.loop_start()
