from fastapi import APIRouter, Depends, HTTPException
import logging

from sqlmodel import Session, select
from taskserver.schemas import TaskReminderBase, UserBase, UserRead
from .database import get_session
from .crud import create_task_reminder, save_user, find_user_by_email_pattern, find_user_by_email
from .models import User

logger = logging.getLogger(__name__)

task_router = APIRouter()
user_router = APIRouter()

def create_error(error_msg: str):
    return HTTPException(status_code=400, detail=error_msg)

@task_router.post("/")
def create_tasks(task_base: TaskReminderBase, session = Depends(get_session)):
    user = find_user_by_email(session, task_base.assignee)
    if not user:
        raise create_error(f"User email {task_base.assignee} does not exist")
    
    task_in_db = create_task_reminder(session, task_base)
    return task_in_db

@task_router.get("/")
def get_tasks():
    return []


@user_router.post("/")
def create_user(user_base: UserBase, session: Session = Depends(get_session)):
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