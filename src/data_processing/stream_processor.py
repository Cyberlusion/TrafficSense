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
from data_storage.db_handler import insert_air_quality_data, get_db
from data_storage.db_handler import insert_gps_data, get_db
from data_storage.db_handler import insert_bluetooth_data, insert_wifi_data, get_db
from data_storage.db_handler import insert_weather_data, get_db
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

#Air quality sensors:

def process_and_store_air_quality_data(pm25, pm10, co2, no2, timestamp, location):
    """
    Process and store air quality sensor data in the database.
    
    Parameters:
    - pm25: Concentration of PM2.5 in micrograms per cubic meter (µg/m³).
    - pm10: Concentration of PM10 in µg/m³.
    - co2: CO2 concentration in parts per million (ppm).
    - no2: NO2 concentration in ppm.
    - timestamp: Timestamp when the data was recorded.
    - location: Location of the air quality sensor.
    """
    with get_db_session() as db:
        stored_record = insert_air_quality_data(db, pm25, pm10, co2, no2, timestamp, location)
        logging.info(f"Stored air quality sensor data: {stored_record}")

def calculate_air_quality_index(pm25, pm10, co2, no2):
    """
    Calculate an overall air quality index based on sensor readings.
    This can be done by aggregating the data or using predefined standards.
    """
    if pm25 > 50 or pm10 > 100 or co2 > 1000 or no2 > 50:
        return "Unhealthy"  # High pollution levels
    elif pm25 > 35 or pm10 > 75 or co2 > 800 or no2 > 40:
        return "Moderate"  # Moderate pollution levels
    else:
        return "Good"  # Good air quality

#GPS:

def process_and_store_gps_data(vehicle_id, latitude, longitude, speed, timestamp):
    """
    Process and store GPS data from vehicles in the database.
    
    Parameters:
    - vehicle_id: Unique identifier for the vehicle.
    - latitude: Latitude of the vehicle's location.
    - longitude: Longitude of the vehicle's location.
    - speed: Speed of the vehicle.
    - timestamp: Timestamp when the data was recorded.
    """
    with get_db_session() as db:
        stored_record = insert_gps_data(db, vehicle_id, latitude, longitude, speed, timestamp)
        logging.info(f"Stored GPS data for Vehicle ID {vehicle_id}: {stored_record}")

def analyze_gps_data(data):
    """
    Perform analysis on GPS data (e.g., identifying traffic patterns, speeds, congestion).
    """
    # Example analysis: Identify traffic jam
    if data["speed"] < 5:  # Speed below 5 km/h indicates congestion
        logging.warning(f"Traffic jam detected near {data['location']}")

#Bluetooth and Wi-Fi:

def process_and_store_bluetooth_data(bluetooth_data):
    """
    Process and store Bluetooth data.
    """
    with get_db_session() as db:
        stored_record = insert_bluetooth_data(db, bluetooth_data)
        logging.info(f"Stored Bluetooth data: {stored_record}")

def process_and_store_wifi_data(wifi_data):
    """
    Process and store Wi-Fi data.
    """
    with get_db_session() as db:
        stored_record = insert_wifi_data(db, wifi_data)
        logging.info(f"Stored Wi-Fi data: {stored_record}")

#Weather data:

def process_and_store_weather_data(weather_data):
    """
    Process and store weather data.
    """
    with get_db_session() as db:
        stored_record = insert_weather_data(db, weather_data)
        logging.info(f"Stored weather data: {stored_record}")

    # Optionally, add conditions to control traffic light or routing based on weather
    if weather_data.get("rainfall") > 10:  # Example condition for heavy rain
        logging.info("Heavy rain detected, adjusting traffic signals for safety.")
        # Additional traffic adjustment actions here, if needed
