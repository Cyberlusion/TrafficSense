# Set Up Air Quality Sensor Data Ingestion

# Air quality sensors may send data with attributes such as PM2.5, PM10, CO2 levels, NO2, timestamp, and sensor location. 
# You can receive this data through protocols like MQTT or HTTP.

import json
import logging
import paho.mqtt.client as mqtt
from data_processing.stream_processor import process_and_store_air_quality_data

def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode("utf-8"))
    sensor_type = payload.get("sensor_type")  # "air_quality"
    pm25 = payload.get("pm25")  # PM2.5 concentration (micrograms per cubic meter)
    pm10 = payload.get("pm10")  # PM10 concentration
    co2 = payload.get("co2")  # CO2 concentration (ppm)
    no2 = payload.get("no2")  # NO2 concentration (ppm)
    timestamp = payload.get("timestamp")
    location = payload.get("location")  # Location of the sensor

    if sensor_type == "air_quality" and pm25 and pm10 and co2 and no2 and timestamp:
        logging.info(f"Received data from {sensor_type} sensor: PM2.5={pm25}, PM10={pm10}, CO2={co2}, NO2={no2}")
        process_and_store_air_quality_data(pm25, pm10, co2, no2, timestamp, location)

def start_air_quality_listener():
    client = mqtt.Client("AirQualityListener")
    client.connect("localhost", 1883)  # MQTT broker address and port
    client.subscribe("traffic/air_quality")
    client.on_message = on_message

    client.loop_start()
