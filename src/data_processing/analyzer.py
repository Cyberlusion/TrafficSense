# src/data_processing/analyzer.py
from config import CONGESTION_THRESHOLD

def analyze_traffic(data):
    """Analyzes traffic data to detect congestion levels."""
    location = data["location"]
    vehicle_count = data["vehicle_count"]

    # Detect congestion
    if vehicle_count > CONGESTION_THRESHOLD:
        analysis_result = {
            "location": location,
            "status": "congested",
            "vehicle_count": vehicle_count
        }
    else:
        analysis_result = {
            "location": location,
            "status": "clear",
            "vehicle_count": vehicle_count
        }
    
    return analysis_result

#  add analysis logic to respond based on the camera data, such as adjusting traffic lights if congestion is detected:

from feedback.feedback_manager import adjust_traffic_light

def analyze_traffic(vehicle_count):
    if vehicle_count > 20:  # Example threshold for congestion
        adjust_traffic_light(light_id="A1", action="green", protocol="mqtt")
