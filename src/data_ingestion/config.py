#This allows easy updates for different environments and decouples configuration from code.

import os

MQTT_BROKER_URL = os.getenv("MQTT_BROKER_URL", "mqtt://broker.hivemq.com")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "iot/traffic")

HTTP_SOURCE_URL = os.getenv("HTTP_SOURCE_URL", "https://api.example.com/traffic")

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "traffic_data")
