# If you haven’t already, define a model in models.py for storing the inductive loop sensor data.

from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class LoopSensorData(Base):
    __tablename__ = "loop_sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    loop_id = Column(String, index=True)
    vehicle_count = Column(Integer)
    occupancy = Column(Integer)
    timestamp = Column(DateTime)
    
class RadarLidarData(Base):
    __tablename__ = "radar_lidar_data"

    id = Column(Integer, primary_key=True, index=True)
    sensor_type = Column(String, index=True)  # Either "radar" or "lidar"
    speed = Column(Float)  # Speed of the detected vehicle
    distance = Column(Float)  # Distance from the sensor
    object_type = Column(String)  # Type of object (e.g., "car", "truck")
    timestamp = Column(DateTime)

class AcousticData(Base):
    __tablename__ = "acoustic_data"

    id = Column(Integer, primary_key=True, index=True)
    sound_level = Column(Float)  # Sound level in decibels (dB)
    vehicle_count = Column(Integer)  # Count of vehicles detected
    timestamp = Column(DateTime)  # Time of the sensor reading

class AirQualityData(Base):
    __tablename__ = "air_quality_data"

    id = Column(Integer, primary_key=True, index=True)
    pm25 = Column(Float)  # PM2.5 concentration (µg/m³)
    pm10 = Column(Float)  # PM10 concentration (µg/m³)
    co2 = Column(Float)  # CO2 concentration (ppm)
    no2 = Column(Float)  # NO2 concentration (ppm)
    timestamp = Column(DateTime)  # Timestamp of data recording
    location = Column(String)  # Location of the sensor

class GPSData(Base):
    __tablename__ = "gps_data"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String, index=True)  # Vehicle identifier
    latitude = Column(Float)  # Latitude of the vehicle
    longitude = Column(Float)  # Longitude of the vehicle
    speed = Column(Float)  # Speed of the vehicle (km/h)
    timestamp = Column(DateTime)  # Timestamp of data recording
