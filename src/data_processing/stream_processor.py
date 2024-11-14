# The stream_processor.py module will be responsible for handling the continuous stream of data and calling the processor.py and analyzer.py functions in real-time.
# You can integrate this with Kafka for seamless data flow.
# src/data_processing/stream_processor.py

import json
import logging
from kafka import KafkaConsumer
from processor import process_data
from analyzer import analyze_traffic
from feedback.feedback_manager import (
    control_traffic_light_via_mqtt,
    control_traffic_light_via_http,
    update_routing_suggestion,
)
from data_storage.db_handler import insert_traffic_data, get_db
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)

@contextmanager
def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

def process_and_store(data):
    # Process data
    processed_data = process_data(data)
    if processed_data:
        # Analyze processed data
        analysis_result = analyze_traffic(processed_data)
        logging.info(f"Analysis result: {analysis_result}")

        # Store in database
        with get_db_session() as db:
            stored_record = insert_traffic_data(db, processed_data)
            logging.info(f"Stored record in database: {stored_record}")

        # Trigger feedback based on analysis results
        if analysis_result.get("congestion_level") > 80:
            control_traffic_light_via_mqtt(light_id="A1", action="green")
            logging.info("Increased green light duration to ease congestion")

        if analysis_result.get("vehicle_count") > 50:
            update_routing_suggestion(vehicle_id="vehicle_123", new_route="Alternate Route")
            logging.info("Updated route for vehicle 123 to avoid congestion")

def start_stream_processing():
    try:
        consumer = KafkaConsumer(
            'traffic_data',
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        logging.info("Kafka consumer connected and waiting for messages...")

        for message in consumer:
            raw_data = message.value
            logging.info(f"Received data: {raw_data}")

            # Process, analyze, store, and handle feedback
            process_and_store(raw_data)

    except Exception as e:
        logging.error(f"Error in stream processing: {e}")

if __name__ == "__main__":
    start_stream_processing()


