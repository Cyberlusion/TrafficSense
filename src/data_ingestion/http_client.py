# If you’re pulling data from an HTTP endpoint instead of MQTT, an HTTP client can be used.

import requests
import time
from kafka_producer import produce_to_kafka
from config import HTTP_SOURCE_URL

def fetch_http_data():
    while True:
        response = requests.get(HTTP_SOURCE_URL)
        if response.status_code == 200:
            data = response.json()
            produce_to_kafka(data)
        time.sleep(60)  # Poll every 60 seconds
