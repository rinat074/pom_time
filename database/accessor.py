from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from settings import settings

engine = create_engine(settings.db_url)

Session = sessionmaker(engine)

def get_db_session() -> Session:
    return Session