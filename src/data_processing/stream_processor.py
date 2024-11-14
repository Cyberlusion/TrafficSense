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
from data_storage.db_handler import insert_loop_sensor_data, get_db
from data_storage.db_handler import insert_radar_lidar_data, get_db
from data_storage.db_handler import insert_acoustic_data, get_db
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

# store camera data:

from data_storage.db_handler import insert_traffic_camera_data, get_db
from contextlib import contextmanager
import logging

@contextmanager
def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

def process_and_store_traffic_camera_data(vehicle_count, congestion_level):
    """
    Process and store traffic camera data into the database.
    
    Parameters:
    - vehicle_count: The number of vehicles detected in the frame.
    - congestion_level: Calculated congestion level.
    """
    with get_db_session() as db:
        stored_record = insert_traffic_camera_data(db, vehicle_count, congestion_level)
        logging.info(f"Stored traffic camera data: {stored_record}")

def analyze_and_store_traffic_camera_data(frame):
    """
    Example analysis function that detects vehicles in a frame and stores
    relevant traffic data into the database.
    
    Parameters:
    - frame: Frame captured from traffic camera.
    """
    vehicle_count = detect_vehicles(frame)  # Assume detect_vehicles is defined
    congestion_level = calculate_congestion_level(vehicle_count)  # Define a calculation function

    # Process and store the data
    process_and_store_traffic_camera_data(vehicle_count, congestion_level)
    logging.info(f"Processed frame with {vehicle_count} vehicles, congestion level: {congestion_level}")

#Add road seonsor data

@contextmanager
def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

def process_and_store_loop_sensor_data(loop_id, vehicle_count, timestamp):
    """
    Process and store inductive loop sensor data in the database.
    
    Parameters:
    - loop_id: Identifier for the inductive loop sensor.
    - vehicle_count: Number of vehicles detected by the sensor.
    - timestamp: Time the data was recorded.
    """
    occupancy = calculate_occupancy(vehicle_count)  # Example function for occupancy

    with get_db_session() as db:
        stored_record = insert_loop_sensor_data(db, loop_id, vehicle_count, occupancy, timestamp)
        logging.info(f"Stored loop sensor data: {stored_record}")

def calculate_occupancy(vehicle_count):
    # Example: Calculate occupancy as a simple function of vehicle count
    return min(100, vehicle_count * 5)  # Assuming each vehicle counts as 5% occupancy

#Add lidar and radar:

def process_and_store_radar_lidar_data(sensor_type, vehicle_data, timestamp):
    """
    Process and store radar or lidar sensor data in the database.
    
    Parameters:
    - sensor_type: Type of sensor ("radar" or "lidar").
    - vehicle_data: List of vehicle data (speed, distance, object type).
    - timestamp: Time the data was recorded.
    """
    for vehicle in vehicle_data:
        speed = vehicle.get("speed")
        distance = vehicle.get("distance")
        object_type = vehicle.get("object_type")

        with get_db_session() as db:
            stored_record = insert_radar_lidar_data(db, sensor_type, speed, distance, object_type, timestamp)
            logging.info(f"Stored {sensor_type} data: {stored_record}")

def calculate_congestion_from_speed(speed):
    """
    Example: Calculate congestion level based on speed.
    Higher speed means less congestion.
    """
    if speed < 20:
        return 90  # High congestion
    elif speed < 40:
        return 60  # Moderate congestion
    else:
        return 30  # Low congestion

#Acoustic sensors:

def process_and_store_acoustic_data(sound_level, vehicle_count, timestamp):
    """
    Process and store acoustic sensor data in the database.
    
    Parameters:
    - sound_level: Measured sound level in decibels (dB).
    - vehicle_count: Count of vehicles detected by the acoustic sensor.
    - timestamp: Timestamp when the data was recorded.
    """
    with get_db_session() as db:
        stored_record = insert_acoustic_data(db, sound_level, vehicle_count, timestamp)
        logging.info(f"Stored acoustic sensor data: {stored_record}")

def calculate_congestion_from_sound_level(sound_level):
    """
    Example: Calculate congestion level based on sound level.
    Higher sound level means higher traffic density.
    """
    if sound_level > 85:
        return 90  # High congestion
    elif sound_level > 70:
        return 60  # Moderate congestion
    else:
        return 30  # Low congestion
