# The stream_processor.py module will be responsible for handling the continuous stream of data and calling the processor.py and analyzer.py functions in real-time.
# You can integrate this with Kafka for seamless data flow.
# src/data_processing/stream_processor.py

from kafka import KafkaConsumer
from processor import process_data
from analyzer import analyze_traffic

import json

from feedback.feedback_manager import (
    control_traffic_light_via_mqtt,
    control_traffic_light_via_http,
    update_routing_suggestion,
)

def start_stream_processing():
    consumer = KafkaConsumer(
        'traffic_data',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        raw_data = message.value
        print(f"Received data: {raw_data}")

        # Process the data
        processed_data = process_data(raw_data)

        # Analyze the data
        if processed_data:
            analysis_result = analyze_traffic(processed_data)
            print(f"Analysis result: {analysis_result}")

# Using data_storage in the Application
#To use this layer, you can import and call functions from db_handler.py wherever you need to store or retrieve traffic data.
#For example, in data_processing/stream_processor.py, you could store processed data like this:

from data_storage.db_handler import insert_traffic_data, get_db
from contextlib import contextmanager

@contextmanager
def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

def process_and_store(data):
    # Process data...
    with get_db_session() as db:
        stored_record = insert_traffic_data(db, data)
        print(f"Stored record: {stored_record}")

def process_traffic_data(data):
    # Example condition: high congestion detected
    if data["congestion_level"] > 80:
        # Change traffic light to green to ease congestion
        control_traffic_light_via_mqtt(light_id="A1", action="green")
        logging.info("Increased green light duration to ease congestion")

    # Example condition: high vehicle count in a specific area
    if data["vehicle_count"] > 50:
        # Reroute vehicles to avoid congested area
        update_routing_suggestion(vehicle_id="vehicle_123", new_route="Alternate Route")
        logging.info("Updated route for vehicle 123 to avoid congestion")

