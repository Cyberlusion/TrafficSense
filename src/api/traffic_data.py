# Creating Traffic Data Endpoints in traffic_data.py
#In traffic_data.py, you will define the actual API endpoints for retrieving, storing, or analyzing traffic data.

# src/api/traffic_data.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from data_storage.db_handler import fetch_recent_data, insert_traffic_data
from data_storage.schema import TrafficData
from .dependencies import get_db

router = APIRouter()

@router.get("/", response_model=List[TrafficData])
def get_traffic_data(limit: int = 100, db: Session = Depends(get_db)):
    """Fetch the most recent traffic data"""
    try:
        data = fetch_recent_data(db, limit)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=TrafficData)
def post_traffic_data(data: dict, db: Session = Depends(get_db)):
    """Insert new traffic data into the database"""
    try:
        inserted_data = insert_traffic_data(db, data)
        return inserted_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
