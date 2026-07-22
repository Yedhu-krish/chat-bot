from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from app.config import DB_HOST,DB_NAME,DB_PORT,DB_PASSWORD,DB_USER


DB_URL = URL.create(
    drivername='postgresql+psycopg',
    database=DB_NAME,
    host=DB_HOST,
    username=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()