# Adding pedestrian counters to your traffic management system is a great idea,
# as it will help improve pedestrian safety by enabling traffic lights and signals to adapt to foot traffic,
# reduce pedestrian wait times, and prioritize pedestrian crossings during high foot traffic periods. 
# These counters use sensors like infrared (IR), stereo cameras, or pressure sensors to detect pedestrians in real time.

# Assume for now that the pedestrian counters use MQTT for real-time data transmission. Create a data ingestion module to listen for pedestrian data.

# src/data_ingestion/pedestrian_counter_client.py

import json
import logging
from mqtt_client import mqtt_client
from data_processing.stream_processor import process_and_store_pedestrian_data

def start_pedestrian_listener():
    def on_message(client, userdata, message):
        try:
            pedestrian_data = json.loads(message.payload.decode())
            logging.info(f"Received pedestrian count data: {pedestrian_data}")
            process_and_store_pedestrian_data(pedestrian_data)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding pedestrian count data: {e}")

    mqtt_client.subscribe("pedestrian/counters")
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()
