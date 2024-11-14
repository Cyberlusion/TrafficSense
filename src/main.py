# src/main.py

from data_ingestion.mqtt_client import start_mqtt_listener
from data_ingestion.http_client import fetch_http_data
from data_processing import start_stream_processing
from data_storage.db_handler import engine
from data_storage.schema import init_db
import threading

def main():
    # Start threads for each data source in the ingestion layer
    mqtt_thread = threading.Thread(target=start_mqtt_listener)
    http_thread = threading.Thread(target=fetch_http_data)

    # Start the data processing thread
    processing_thread = threading.Thread(target=start_stream_processing)

    # Start all threads
    mqtt_thread.start()
    http_thread.start()
    processing_thread.start()

    # Wait for all threads to complete
    mqtt_thread.join()
    http_thread.join()
    processing_thread.join()

if __name__ == "__main__":
    # Initialize database tables
    init_db(engine)
    # Start the rest of the application
    main()
