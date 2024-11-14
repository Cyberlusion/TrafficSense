#This module will handle database connections and basic CRUD (Create, Read, Update, Delete) operations.
#For this example, let’s assume a PostgreSQL database and use SQLAlchemy for ORM (Object-Relational Mapping), which abstracts SQL commands and makes database operations simpler.

# src/data_storage/db_handler.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from .schema import TrafficData
from .models import RadarLidarData
from .models import AcousticData
from .models import AirQualityData
from .models import GPSData
from .models import BluetoothData, WifiData
from .models import WeatherData
from .models import TrafficLightAction
from .models import PedestrianData
from .models import EdgeDeviceData

# Set up the database connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create an engine and a session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def insert_traffic_data(db, data):
    """Inserts a new traffic data record."""
    new_record = TrafficData(**data)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def fetch_recent_data(db, limit=100):
    """Fetches the most recent traffic data records."""
    return db.query(TrafficData).order_by(TrafficData.timestamp.desc()).limit(limit).all()

#Add a function to insert traffic camera data into the database. 
#For example, we’ll assume you have a traffic_data table with columns like timestamp, vehicle_count, and congestion_level.

from sqlalchemy.orm import Session
from datetime import datetime
from .models import TrafficData

def insert_traffic_camera_data(db: Session, vehicle_count: int, congestion_level: int):
    """
    Inserts traffic camera data into the database.
    
    Parameters:
    - db: Database session.
    - vehicle_count: The number of vehicles detected.
    - congestion_level: Calculated congestion level.
    """
    new_record = TrafficData(
        timestamp=datetime.utcnow(),
        vehicle_count=vehicle_count,
        congestion_level=congestion_level
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

#Add road sensors:

from sqlalchemy.orm import Session
from datetime import datetime
from .models import LoopSensorData

def insert_loop_sensor_data(db: Session, loop_id: str, vehicle_count: int, occupancy: int, timestamp: str):
    """
    Inserts inductive loop sensor data into the database.
    
    Parameters:
    - db: Database session.
    - loop_id: ID of the loop sensor.
    - vehicle_count: Number of vehicles detected.
    - occupancy: Calculated occupancy percentage.
    - timestamp: Timestamp of the sensor reading.
    """
    new_record = LoopSensorData(
        loop_id=loop_id,
        vehicle_count=vehicle_count,
        occupancy=occupancy,
        timestamp=datetime.fromisoformat(timestamp)
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

#add radar and lidar:

def insert_radar_lidar_data(db: Session, sensor_type: str, speed: float, distance: float, object_type: str, timestamp: str):
    """
    Inserts radar or lidar sensor data into the database.
    
    Parameters:
    - db: Database session.
    - sensor_type: Type of sensor ("radar" or "lidar").
    - speed: Speed of the detected vehicle.
    - distance: Distance from the sensor.
    - object_type: Type of the object (e.g., "car", "truck").
    - timestamp: Timestamp of the reading.
    """
    new_record = RadarLidarData(
        sensor_type=sensor_type,
        speed=speed,
        distance=distance,
        object_type=object_type,
        timestamp=datetime.fromisoformat(timestamp)
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

#acoustic sensors:

def insert_acoustic_data(db: Session, sound_level: float, vehicle_count: int, timestamp: str):
    """
    Inserts acoustic sensor data into the database.
    
    Parameters:
    - db: Database session.
    - sound_level: Measured sound level in decibels (dB).
    - vehicle_count: Count of vehicles detected.
    - timestamp: Timestamp when the data was recorded.
    """
    new_record = AcousticData(
        sound_level=sound_level,
        vehicle_count=vehicle_count,
        timestamp=datetime.fromisoformat(timestamp)
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

#Air quality sensors:

ef insert_air_quality_data(db: Session, pm25: float, pm10: float, co2: float, no2: float, timestamp: str, location: str):
    """
    Inserts air quality sensor data into the database.
    
    Parameters:
    - db: Database session.
    - pm25: PM2.5 concentration in µg/m³.
    - pm10: PM10 concentration in µg/m³.
    - co2: CO2 concentration in ppm.
    - no2: NO2 concentration in ppm.
    - timestamp: Timestamp of data.
    - location: Location of the sensor.
    """
    new_record = AirQualityData(
        pm25=pm25,
        pm10=pm10,
        co2=co2,
        no2=no2,
        timestamp=datetime.fromisoformat(timestamp),
        location=location
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

#GPS:

def insert_gps_data(db: Session, vehicle_id: str, latitude: float, longitude: float, speed: float, timestamp: str):
    """
    Inserts GPS data into the database.
    
    Parameters:
    - db: Database session.
    - vehicle_id: Unique identifier for the vehicle.
    - latitude: Latitude of the vehicle's location.
    - longitude: Longitude of the vehicle's location.
    - speed: Speed of the vehicle.
    - timestamp: Timestamp of data.
    """
    new_record = GPSData(
        vehicle_id=vehicle_id,
        latitude=latitude,
        longitude=longitude,
        speed=speed,
        timestamp=datetime.fromisoformat(timestamp)
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

#Wi-fi and Bluetooth:

def insert_bluetooth_data(db: Session, bluetooth_data: dict):
    new_record = BluetoothData(
        device_id=bluetooth_data["device_id"],
        rssi=bluetooth_data["rssi"],
        timestamp=bluetooth_data["timestamp"],
        location_latitude=bluetooth_data["location"]["latitude"],
        location_longitude=bluetooth_data["location"]["longitude"],
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def insert_wifi_data(db: Session, wifi_data: dict):
    new_record = WifiData(
        mac_address=wifi_data["mac_address"],
        rssi=wifi_data["rssi"],
        timestamp=wifi_data["timestamp"],
        location_latitude=wifi_data["location"]["latitude"],
        location_longitude=wifi_data["location"]["longitude"],
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

#weather:

def insert_weather_data(db: Session, weather_data: dict):
    new_record = WeatherData(
        temperature=weather_data.get("temperature"),
        humidity=weather_data.get("humidity"),
        pressure=weather_data.get("pressure"),
        rainfall=weather_data.get("rainfall"),
        wind_speed=weather_data.get("wind_speed"),
        timestamp=weather_data.get("timestamp"),
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

# Smart traffic lights:

def log_traffic_light_action(db: Session, light_id: str, action: str):
    action_record = TrafficLightAction(light_id=light_id, action=action)
    db.add(action_record)
    db.commit()
    db.refresh(action_record)
    return action_record

#pedestrians:

def insert_pedestrian_data(db: Session, pedestrian_data: dict):
    new_record = PedestrianData(
        count=pedestrian_data.get("count"),
        location_id=pedestrian_data.get("location_id"),
        timestamp=pedestrian_data.get("timestamp")
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

#AI edge:

def insert_edge_device_data(db: Session, edge_data: dict):
    new_record = EdgeDeviceData(
        device_id=edge_data.get("device_id"),
        object_detected=edge_data.get("object"),
        confidence=edge_data.get("confidence"),
        timestamp=edge_data.get("timestamp")
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record
