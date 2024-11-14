#Define the schema for the TrafficData table or collection, depending on your database choice. This will provide a structure for the data you’re storing.

# src/data_storage/schema.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class TrafficData(Base):
    """SQLAlchemy ORM model for storing traffic data."""
    __tablename__ = "traffic_data"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    vehicle_count = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Initialize the database with this model
def init_db(engine):
    Base.metadata.create_all(bind=engine)
