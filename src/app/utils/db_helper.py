import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.utils.constants import DB_URL
from src.app.models.event_model import Base, Event

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)

class DBHelper:
    def __init__(self):
        self.db = SessionLocal()

    def insert_event(self, event_name: str, user_id: int):
        new_event = Event(event_name=event_name, user_id=user_id)
        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)