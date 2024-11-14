# Setting Up Feedback Functions for IoT Devices
# Here’s a basic outline for feedback functions, using MQTT to send commands and HTTP for systems that might not support MQTT:

import paho.mqtt.client as mqtt
import requests
import logging

# MQTT Configuration
MQTT_BROKER = "mqtt_broker_address"
MQTT_PORT = 1883
MQTT_TOPIC_TRAFFIC_LIGHT = "traffic/control/light"

# HTTP Configuration
TRAFFIC_LIGHT_API_URL = "http://traffic-system.local/api/traffic_light"

# Initialize the MQTT client
mqtt_client = mqtt.Client()

def connect_mqtt():
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        mqtt_client.loop_start()
        logging.info("Connected to MQTT broker")
    except Exception as e:
        logging.error(f"MQTT connection failed: {e}")

def control_traffic_light_via_mqtt(light_id, action):
    """Sends a control command to a traffic light via MQTT."""
    try:
        message = {"light_id": light_id, "action": action}  # action could be "green", "red", "yellow"
        mqtt_client.publish(MQTT_TOPIC_TRAFFIC_LIGHT, str(message))
        logging.info(f"Sent MQTT command to traffic light {light_id}: {action}")
    except Exception as e:
        logging.error(f"Failed to send MQTT command: {e}")

def control_traffic_light_via_http(light_id, action):
    """Sends a control command to a traffic light via HTTP."""
    try:
        payload = {"light_id": light_id, "action": action}
        response = requests.post(f"{TRAFFIC_LIGHT_API_URL}/control", json=payload)
        response.raise_for_status()
        logging.info(f"Sent HTTP command to traffic light {light_id}: {action}")
    except requests.RequestException as e:
        logging.error(f"Failed to send HTTP command: {e}")

def update_routing_suggestion(vehicle_id, new_route):
    """Sends a routing suggestion to a vehicle or GPS system."""
    # Assuming there’s an API endpoint to send route updates to GPS devices
    gps_update_url = f"http://gps-system.local/api/vehicles/{vehicle_id}/route"
    try:
        payload = {"new_route": new_route}
        response = requests.put(gps_update_url, json=payload)
        response.raise_for_status()
        logging.info(f"Updated route for vehicle {vehicle_id}")
    except requests.RequestException as e:
        logging.error(f"Failed to update route for vehicle {vehicle_id}: {e}")
