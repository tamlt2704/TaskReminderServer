from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
import logging

from sqlmodel import Session, select
from taskserver.auth import get_current_active_user
from taskserver.schemas import TaskReminderCreate, TaskUpdate, UserCreate, UserRead
from .database import get_session
from .crud import create_task_reminder, delete_task_by_id, find_user_by_username, save_user, find_user_by_email_pattern, get_all_tasks, get_task_by_id, update_task_in_db
from .models import User

logger = logging.getLogger(__name__)

task_router = APIRouter()
user_router = APIRouter()

def create_error(error_msg: str):
    return HTTPException(status_code=400, detail=error_msg)

@task_router.post("/")
def create_tasks(task_base: TaskReminderCreate, session = Depends(get_session), user: UserRead = Depends(get_current_active_user)):
    assignee = find_user_by_username(session, task_base.assignee)
    if not assignee:
        raise create_error(f"User name {task_base.assignee} does not exist")
    
    task_in_db = create_task_reminder(session, task_base, user)
    return task_in_db

@task_router.get("/{task_id}")
def fetch_task(task_id: int, session: Session = Depends(get_session)):
    task_in_db = get_task_by_id(session, task_id)
    if not task_in_db:
        raise create_error(f"Task with id: {task_id} does not exist")
    
    return task_in_db

@task_router.put("/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate, session: Session = Depends(get_session), user: UserRead = Depends(get_current_active_user)):
    task_in_db = get_task_by_id(session, task_id)
    if not task_in_db:
        raise create_error(f"Task with id: {task_id} does not exist")
    updated_task = update_task_in_db(session, user, task_in_db, updated_task)
    return updated_task

@task_router.delete("/{task_id}")
def remove_task(task_id: int, session: Session = Depends(get_session), user: UserRead = Depends(get_current_active_user)):
    return delete_task_by_id(session, task_id)

@task_router.get("/usertask/{user_name}")
def get_tasks(user_name: str, session: Session = Depends(get_session)):
    return get_all_tasks(session, user_name)

@user_router.post("/")
def create_user(user_base: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).filter_by(email=user_base.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    try:
        user_db = save_user(session, user_base)
        public_user = UserRead(**user_db.model_dump(exclude={"hasshed_password", "id"}))
    except Exception as e:
        logger.error(e)
        return {"message": "Failed to create user", "user": None}
    return {"message": "Success", "user": public_user}

@user_router.get("/search/{email_pattern}")
def search_users_by_email(email_pattern: str, session: Session = Depends(get_session)):
    user_list_in_db = find_user_by_email_pattern(session, email_pattern)
    public_users = [UserRead(**user_db.model_dump(exclude={"hasshed_password", "id"})) for user_db in user_list_in_db]
    return public_users