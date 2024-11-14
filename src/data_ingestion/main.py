# To make it easy to start the ingestion process, create a main.py script:

from data_ingestion.mqtt_client import start_mqtt_listener
from data_ingestion.http_client import fetch_http_data
import threading

if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=start_mqtt_listener)
    http_thread = threading.Thread(target=fetch_http_data)
    
    mqtt_thread.start()
    http_thread.start()

    mqtt_thread.join()
    http_thread.join()
