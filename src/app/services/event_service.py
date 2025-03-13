from sqlalchemy.orm import Session
from src.app.models.event_model import Event
from src.app.utils.cache_helper import (
    get_cache_events, set_cached_events
)

class EventService:

    def __init__(self, db: Session):
        self.db = db

    def add_event_data(self,event_data):
        event_name = event_data["event"]
        user_id = event_data["user_id"]
        new_event = Event(event_name=event_name, user_id=user_id)
        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)

    def get_event_data(self, event_name: str = None, limit: int = 10, offset: int = 0):
        cache_key = f"events:{event_name}:{limit}:{offset}"
        cached_data = get_cache_events(key=cache_key)
        if cached_data:
            return cached_data
        query = self.db.query(Event)
        if event_name:
            query = query.filter(Event.event_name == event_name)
        events = query.offset(offset).limit(limit).all()
        resp_data = [{"event_name": event.event_name, "user_id": event.user_id} for event in events]
        set_cached_events(key=cache_key, data=resp_data)
        return resp_data

