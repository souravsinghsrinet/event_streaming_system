from fastapi import APIRouter, Depends, status
from src.app.utils.kafka_helper import KafkaHelper

track_event_router = APIRouter(
    prefix="/v1/track-event",
    tags=["add_data"],
    responses={
        404: {"description": "Not found"}
    }
)

@track_event_router.post("")
def track_event(event_name: str, user_id: int):
    event_data = {"event": event_name, "user_id": user_id}
    k_h_obj = KafkaHelper()
    k_h_obj.send_event(topic="user_events", data=event_data)
    return {"message": "Event sent successfully!"}

