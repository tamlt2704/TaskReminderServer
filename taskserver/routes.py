from fastapi import APIRouter, Depends
import logging
from taskserver.schemas import TaskReminderBase
from .database import get_session
from .crud import create_task_reminder

logger = logging.getLogger(__name__)

task_router = APIRouter()
user_router = APIRouter()

@task_router.post("/")
def create_tasks(task_base: TaskReminderBase, session = Depends(get_session)):
    logger.info(f'save {task_base}')
    task_in_db = create_task_reminder(session, task_base)
    return task_in_db

@task_router.get("/")
def get_tasks():
    return []


@user_router.get("/")
def get_users():
    return []