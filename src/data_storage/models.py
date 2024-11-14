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
