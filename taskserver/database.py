from sqlmodel import create_engine, Session, SQLModel
import os
from dotenv import load_dotenv
import logging
from .models import * # for the init-db to work

logger = logging.getLogger(__name__)

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    logger.info('init database')
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session