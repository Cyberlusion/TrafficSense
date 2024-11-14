#This module will handle database connections and basic CRUD (Create, Read, Update, Delete) operations.
#For this example, let’s assume a PostgreSQL database and use SQLAlchemy for ORM (Object-Relational Mapping), which abstracts SQL commands and makes database operations simpler.

# src/data_storage/db_handler.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from .schema import TrafficData

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
