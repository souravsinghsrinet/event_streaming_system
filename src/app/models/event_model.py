from sqlalchemy import (
    Column, Integer, String,
    TIMESTAMP, func
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

