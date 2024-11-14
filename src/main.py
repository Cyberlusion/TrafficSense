from fastapi import FastAPI
from data_ingestion.mqtt_client import start_mqtt_listener
from data_ingestion.http_client import fetch_http_data
from data_processing import start_stream_processing
from data_storage.db_handler import engine
from data_storage.schema import init_db
from api.traffic_data import router as traffic_data_router
from api.dependencies import get_db

import threading

def start_background_tasks():
    """Start all background tasks (data ingestion and processing)."""
    # Start threads for each data source in the ingestion layer
    mqtt_thread = threading.Thread(target=start_mqtt_listener, name="MQTT Listener")
    http_thread = threading.Thread(target=fetch_http_data, name="HTTP Data Fetcher")
    
    # Start the data processing thread
    processing_thread = threading.Thread(target=start_stream_processing, name="Data Processing")
    
    # Start all threads
    mqtt_thread.start()
    http_thread.start()
    processing_thread.start()

    # Wait for all threads to complete
    mqtt_thread.join()
    http_thread.join()
    processing_thread.join()

def create_app() -> FastAPI:
    """Initialize and return the FastAPI application."""
    app = FastAPI()

    # Include the traffic data routes
    app.include_router(traffic_data_router, prefix="/traffic_data", tags=["traffic_data"])

    # Optional: Include health check route
    @app.get("/health")
    def read_health():
        return {"status": "ok"}

    return app

def init_app():
    """Initialize the app: Database setup, and background task startup."""
    # Initialize the database tables
    init_db(engine)
    
    # Start the background tasks (threads for data ingestion and processing)
    start_background_tasks()

if __name__ == "__main__":
    # Initialize application
    init_app()

    # Start FastAPI app
    app = create_app()
    # FastAPI will automatically run when you call uvicorn with `app`
