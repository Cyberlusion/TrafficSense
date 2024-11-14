#In the central server, set up an MQTT client to receive data from edge devices and trigger relevant actions based on the processed information. 
#For example, if an edge device reports high congestion or an accident, the central system can adjust traffic lights.

# src/data_ingestion/edge_data_listener.py

import json
import logging
from mqtt_client import mqtt_client
from data_processing.stream_processor import process_edge_device_data

def start_edge_device_listener():
    def on_message(client, userdata, message):
        try:
            edge_data = json.loads(message.payload.decode())
            logging.info(f"Received edge device data: {edge_data}")
            process_edge_device_data(edge_data)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding edge device data: {e}")

    mqtt_client.subscribe("edge_device/traffic_data")
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()
