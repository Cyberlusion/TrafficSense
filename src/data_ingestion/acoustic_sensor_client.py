#Set Up Acoustic Sensor Data Ingestion

#Acoustic sensors might send data with a variety of attributes, such as sound level (decibels), vehicle count, and timestamp. 
#These could be sent over MQTT, HTTP, or another protocol.

import json
import logging
import paho.mqtt.client as mqtt
from data_processing.stream_processor import process_and_store_acoustic_data

def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode("utf-8"))
    sensor_type = payload.get("sensor_type")  # "acoustic"
    sound_level = payload.get("sound_level")  # Decibels
    vehicle_count = payload.get("vehicle_count")  # Count of vehicles detected
    timestamp = payload.get("timestamp")

    if sensor_type == "acoustic" and sound_level and vehicle_count and timestamp:
        logging.info(f"Received data from {sensor_type} sensor: Sound Level={sound_level}dB, Vehicle Count={vehicle_count}")
        process_and_store_acoustic_data(sound_level, vehicle_count, timestamp)

def start_acoustic_listener():
    client = mqtt.Client("AcousticListener")
    client.connect("localhost", 1883)  # MQTT broker address and port
    client.subscribe("traffic/acoustic")
    client.on_message = on_message

    client.loop_start()
