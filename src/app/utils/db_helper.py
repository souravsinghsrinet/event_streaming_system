import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.app.utils.constants import DB_URL

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DBHelper:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="event_db",
            user="user",
            password="password",
            host="postgres",
            port="5432"
        )
        self.cursor = self.conn.cursor()

    def insert_event(self, event_name: str, user_id: int):
        self.cursor.execute(
            "INSERT INTO events (event_name, user_id) VALUES (%s, %s)",
            (event_name, user_id)
        )
        self.conn.commit()