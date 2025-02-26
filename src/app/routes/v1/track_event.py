from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from src.app.utils.kafka_helper import KafkaHelper
from src.app.utils.db_helper import get_db
from src.app.services.event_service import EventService

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


@track_event_router.get("")
def get_events(event_name: str = None, limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    e_s_obj = EventService(db=db)
    resp = e_s_obj.get_event_data(event_name=event_name, limit=limit, offset=offset)
    resp_data = [{"event_name": i.event_name, "user_id": i.user_id} for i in resp]
    return JSONResponse(
        {
            "status": "success",
            "data": resp_data
        },
        status_code=status.HTTP_200_OK
    )



