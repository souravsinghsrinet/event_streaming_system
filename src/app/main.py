from fastapi import FastAPI
from src.app.routes.v1 import track_event_router
from threading import Thread
from src.app.utils.kafka_helper import KafkaHelper


def start_consumer():
    k_h_obj = KafkaHelper()
    k_h_obj.consume_events()


consumer_thread = Thread(target=start_consumer, daemon=True)
consumer_thread.start()

app = FastAPI(debug=True)

app.include_router(track_event_router)



