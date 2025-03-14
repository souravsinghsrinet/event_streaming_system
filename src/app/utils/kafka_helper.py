from kafka import KafkaProducer, KafkaConsumer
import json
import time
from src.app.utils.db_helper import get_db
from src.app.utils.constants import KAFKA_BROKER
from src.app.services.event_service import EventService
from src.app.services.websocket_service import notify_clients
import asyncio


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

        self.consumer = KafkaConsumer(
            "user_events",
            bootstrap_servers=KAFKA_BROKER,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            enable_auto_commit=False,  # Disable auto commit for better control
            auto_offset_reset="earliest",
            group_id="event_consumer_group"  # ✅ Add a group_id
        )

        self.db = next(get_db())

    def send_event(self, topic: str, data: dict):
        self.producer.send(topic, data)

    def consume_events(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        while True:
            try:
                messages = self.consumer.poll(timeout_ms=1000)  # Poll messages in batches
                if messages:
                    for _, records in messages.items():
                        for message in records:
                            event_data = message.value
                            print(f"Processing event: {event_data}")

                            # Retry logic
                            for attempt in range(3):
                                try:
                                    e_s_obj = EventService(db=self.db)
                                    e_s_obj.add_event_data(event_data=event_data)
                                    self.consumer.commit()  # Commit offset after successful processing
                                    print(f"✅ Event stored: {event_data}")

                                    # Notify WebSocket clients
                                    loop.run_until_complete(notify_clients(event_data))
                                    break  # Exit retry loop on success

                                except Exception as e:
                                    print(f"❌ Error processing event (Attempt {attempt + 1}/3): {e}")
                                    time.sleep(2)  # Wait before retrying
            except Exception as e:
                print(f"❌ Kafka consumer error: {e}")
                time.sleep(5)  # Wait before retrying

