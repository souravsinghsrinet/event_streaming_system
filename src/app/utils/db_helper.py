from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.utils.constants import DB_URL
from src.app.models.event_model import Base

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()