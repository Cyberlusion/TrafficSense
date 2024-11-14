# src/data_processing/processor.py
import json
from datetime import datetime
from config import AGGREGATION_INTERVAL
from kafka_producer import produce_to_kafka

def process_data(raw_data):
    """Transforms raw telemetry data for analysis."""
    try:
        # Parse JSON data
        data = json.loads(raw_data)
        
        # Extract fields (example fields: 'location', 'vehicle_count', 'timestamp')
        timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
        location = data["location"]
        vehicle_count = int(data["vehicle_count"])

        # Aggregate or transform data if necessary
        # For example, you might want to aggregate vehicle counts by location

        # Placeholder: send processed data to the analysis module or a Kafka topic
        aggregated_data = {
            "location": location,
            "vehicle_count": vehicle_count,
            "timestamp": timestamp
        }
        
        # Send processed data to Kafka for analysis
        produce_to_kafka(aggregated_data)

    except Exception as e:
        print(f"Failed to process data: {e}")
