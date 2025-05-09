import logging
from fastapi import FastAPI
from taskreminder.services import TaskService, UserService
from taskreminder.dao import TaskDao, UserDao
from taskreminder.models import *
from .db import engine
from contextlib import asynccontextmanager


logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


task_dao = TaskDao(engine)
task_service = TaskService(task_dao)

user_dao = UserDao(engine)
user_service = UserService(user_dao)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")
    SQLModel.metadata.create_all(engine)
    yield
    logger.info("Shutting down the application...")

app = FastAPI(lifespan=lifespan)