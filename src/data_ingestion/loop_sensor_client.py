#Set Up Sensor Data Ingestion

#For this example, let’s assume the sensors send data via MQTT with each message containing the loop ID, vehicle count, and timestamp.

import json
import logging
import paho.mqtt.client as mqtt
from data_processing.stream_processor import process_and_store_loop_sensor_data

def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode("utf-8"))
    loop_id = payload.get("loop_id")
    vehicle_count = payload.get("vehicle_count")
    timestamp = payload.get("timestamp")

    if loop_id and vehicle_count is not None:
        logging.info(f"Received data from loop sensor {loop_id}: vehicle_count={vehicle_count}")
        process_and_store_loop_sensor_data(loop_id, vehicle_count, timestamp)

def start_loop_sensor_listener():
    client = mqtt.Client("LoopSensorListener")
    client.connect("localhost", 1883)  # MQTT broker address and port
    client.subscribe("traffic/loop_sensors")
    client.on_message = on_message

    client.loop_start()
