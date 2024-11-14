# AI Model Deployment on Edge Device

# To deploy a model for vehicle and pedestrian detection, you can use a lightweight, pre-trained model compatible with edge AI devices, such as YOLOv5 or MobileNet SSD for object detection.
# For this example, assume YOLOv5 is used. You’ll need to load the model and process real-time frames from connected cameras.

# edge_device/ai_processor.py

import torch
import cv2
import json
import paho.mqtt.client as mqtt

# Load the pre-trained YOLO model for real-time object detection
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Load a small version of YOLO for edge

# MQTT setup for communicating results
client = mqtt.Client()
client.connect("central_server", 1883, 60)  # Replace with the actual central server address

def detect_and_publish():
    # Capture video frames from the camera
    cap = cv2.VideoCapture(0)  # Replace '0' with actual camera feed if needed
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform object detection
        results = model(frame)
        predictions = results.pandas().xyxy[0]  # Extract predictions in Pandas DataFrame format

        # Filter and format detected objects
        processed_data = []
        for _, row in predictions.iterrows():
            label, confidence = row['name'], row['confidence']
            if label in ['car', 'person'] and confidence > 0.5:
                processed_data.append({"object": label, "confidence": confidence})

        # Publish results to central system via MQTT
        if processed_data:
            client.publish("edge_device/traffic_data", json.dumps(processed_data))
            print(f"Published data: {processed_data}")

    cap.release()
    client.disconnect()
