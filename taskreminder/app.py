import logging
from fastapi import FastAPI
from taskreminder.services import TaskService
from taskreminder.dao import TaskDao
from taskreminder.models import *
from .db import engine


logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

SQLModel.metadata.create_all(engine)
task_dao = TaskDao(engine)
task_service = TaskService(task_dao)

app = FastAPI()
logger.info('application init done.')