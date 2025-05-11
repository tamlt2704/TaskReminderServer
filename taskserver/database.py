from sqlmodel import create_engine, Session, SQLModel
import os
from dotenv import load_dotenv
import logging
from .models import * # for the init-db to work
import os

logger = logging.getLogger(__name__)

load_dotenv()
db_filename = 'db.sqlite3'
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///./{db_filename}")
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    logger.info('init database')
    if os.path.exists(db_filename):
        logger.info(f'removing file {db_filename}')
        os.remove(db_filename)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session