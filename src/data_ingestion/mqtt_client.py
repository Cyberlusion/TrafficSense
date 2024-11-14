# Set up an MQTT client to subscribe to data from IoT sensors.

import paho.mqtt.client as mqtt
from kafka_producer import produce_to_kafka

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    # Process the incoming message
    data = msg.payload.decode()
    print(f"Received message: {data}")
    produce_to_kafka(data)

def start_mqtt_listener():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER_URL)

    # Blocking call that processes network traffic, dispatches callbacks, and handles reconnecting
    client.loop_forever()
