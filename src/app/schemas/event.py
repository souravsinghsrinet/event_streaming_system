from pydantic import BaseModel


class EventResponse(BaseModel):
    event_name: str
    user_id: int