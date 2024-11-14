# We’ll use kafka-python to send data to Kafka, enabling smooth streaming for the processing layer.

from kafka import KafkaProducer
import json
from config import KAFKA_BROKER, KAFKA_TOPIC

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def produce_to_kafka(data):
    try:
        producer.send(KAFKA_TOPIC, value=data)
        print(f"Sent to Kafka: {data}")
    except Exception as e:
        print(f"Failed to send to Kafka: {e}")
