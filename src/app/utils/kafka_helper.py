from kafka import KafkaProducer, KafkaConsumer
import json
import time
from src.app.utils.db_helper import DBHelper
from src.app.utils.constants import KAFKA_BROKER

# Retry mechanism to wait for Kafka to be ready
def wait_for_kafka():
    max_retries = 10
    for i in range(max_retries):
        try:
            producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
            producer.close()
            print("✅ Kafka is available!")
            return
        except Exception as e:
            print(f"❌ Kafka not available yet ({i+1}/{max_retries} retries)...")
            time.sleep(5)
    raise Exception("Kafka is not available after multiple retries.")

# Wait for Kafka before initializing producers and consumers
wait_for_kafka()


class KafkaHelper:
    def __init__(self):
        # Kafka Producer
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        # Kafka Consumer
        self.consumer = KafkaConsumer(
            "user_events",
            bootstrap_servers=KAFKA_BROKER,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )

        # Database Helper
        self.db_helper = DBHelper()

    def send_event(self, topic: str, data: dict):
        self.producer.send(topic, data)

    def consume_events(self):
        for message in self.consumer:
            event_data = message.value
            self.db_helper.insert_event(event_data["event"], event_data["user_id"])
            print(f"Stored event: {event_data}")
