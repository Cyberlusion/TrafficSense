# Define Communication Protocols with Smart Traffic Lights

# Assuming the traffic lights support both MQTT and HTTP, you can create modules in src/feedback/traffic_light_controller.py to interact with them.

# src/feedback/traffic_light_controller.py

import logging
import json
import requests
from mqtt_client import mqtt_client

# Function to control traffic light via MQTT
def control_traffic_light_via_mqtt(light_id, action):
    topic = f"traffic_lights/{light_id}/control"
    message = json.dumps({"action": action})
    mqtt_client.publish(topic, message)
    logging.info(f"Sent MQTT command to {light_id}: {action}")

# Function to control traffic light via HTTP
def control_traffic_light_via_http(light_id, action, api_url):
    try:
        response = requests.post(
            f"{api_url}/traffic_lights/{light_id}/control",
            json={"action": action}
        )
        if response.status_code == 200:
            logging.info(f"HTTP control command sent to {light_id}: {action}")
        else:
            logging.error(f"Failed to send HTTP command to {light_id}: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"HTTP control command failed: {e}")

#include pedestrians:

def control_traffic_light_for_pedestrians(light_id, action):
    topic = f"traffic_lights/{light_id}/pedestrian_control"
    message = json.dumps({"action": action})
    mqtt_client.publish(topic, message)
    logging.info(f"Sent pedestrian priority command to {light_id}: {action}")

#Adding AI Edge:

def handle_edge_alerts(light_id, action):
    """
    Example command to control lights based on data from edge devices.
    """
    topic = f"traffic_lights/{light_id}/control"
    message = json.dumps({"action": action})
    mqtt_client.publish(topic, message)
    logging.info(f"Traffic light {light_id} set to {action} based on edge data")
