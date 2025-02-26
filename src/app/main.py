from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.app.routes.v1 import track_event_router
from threading import Thread
from src.app.utils.kafka_helper import KafkaHelper
from src.app.utils.db_helper import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔧 Creating tables before the app starts...")
    create_tables()
    print("✅ Tables verified successfully!")
    yield  # Continue running the app

def start_consumer():
    k_h_obj = KafkaHelper()
    k_h_obj.consume_events()


consumer_thread = Thread(target=start_consumer, daemon=True)
consumer_thread.start()

app = FastAPI(lifespan=lifespan)

app.include_router(track_event_router)



