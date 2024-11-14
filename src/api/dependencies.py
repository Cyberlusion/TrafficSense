#Handling Database Dependencies in dependencies.py
#The dependencies.py file will define reusable dependencies like the database session that can be injected into the API endpoints using FastAPI’s Depends.

# src/api/dependencies.py

from sqlalchemy.orm import Session
from data_storage.db_handler import get_db as db_session

# Reuse the get_db function from the data_storage module
def get_db() -> Session:
    db = next(db_session())
    try:
        yield db
    finally:
        db.close()
