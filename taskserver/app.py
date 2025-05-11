from fastapi import FastAPI
import logging
import logging.config
from contextlib import asynccontextmanager
from .database import init_db

logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")
    init_db()
    yield
    logger.info("Shutting down the application...")

app = FastAPI(lifespan=lifespan)

@app.get('/')
def index():
    return 'TaskReminderServer'