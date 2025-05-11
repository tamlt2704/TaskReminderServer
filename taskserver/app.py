from fastapi import FastAPI
import logging
import logging.config
from contextlib import asynccontextmanager
from .database import init_db
from .routes import task_router, user_router

logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")
    init_db()
    yield
    logger.info("Shutting down the application...")

app = FastAPI(lifespan=lifespan)
app.include_router(task_router, prefix="/api/v1/tasks")
app.include_router(user_router, prefix="/api/v1/users")

@app.get('/')
def index():
    return 'TaskReminderServer'