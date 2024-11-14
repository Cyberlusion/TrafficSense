# If you haven’t already, define a model in models.py for storing the inductive loop sensor data.

from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class LoopSensorData(Base):
    __tablename__ = "loop_sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    loop_id = Column(String, index=True)
    vehicle_count = Column(Integer)
    occupancy = Column(Integer)
    timestamp = Column(DateTime)
