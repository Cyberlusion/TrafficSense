# src/api/main.py

from fastapi import FastAPI
from .traffic_data import router as traffic_data_router
from .dependencies import get_db

app = FastAPI()

# Include the traffic data routes
app.include_router(traffic_data_router, prefix="/traffic_data", tags=["traffic_data"])

# Optional: Include health check route
@app.get("/health")
def read_health():
    return {"status": "ok"}
