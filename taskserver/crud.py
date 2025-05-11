
from datetime import datetime, timezone
from sqlmodel import Session, delete, select

from taskserver.schemas import TaskReminderCreate, UserBase, UserCreate, TaskUpdate
from taskserver.models import TaskReminder, User
from .auth_util import get_password_hash

def update_task_in_db(session: Session, user: User, task: TaskReminder, update_data: TaskUpdate):
    updated_task = task.model_copy(update=update_data.model_dump(exclude_none=True))
    updated_task.set_modified_by(user)
    updated_task.updated_at = datetime.now(timezone.utc)
    session.add(updated_task)
    session.commit()
    session.refresh(updated_task)
    return updated_task
    

def create_task_reminder(session: Session, data: TaskReminderCreate, user: User):
    reminder: TaskReminder = TaskReminder.model_validate(data)        
    reminder.set_created_by(user)
    session.add(reminder)
    session.commit()
    session.refresh(reminder)
    return reminder

def save_user(session: Session, user_data: UserCreate):
    user: User = User.model_validate(user_data)
    user.hashed_password = get_password_hash(user_data.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def find_user_by_email_pattern(session: Session, email_pattern: str):
    users = session.exec(select(User).where(User.email.like(f"%{email_pattern}%"))).all()
    return users if users else {"error": "No users found"}

def find_user_by_email(session, email):
    return session.exec(select(User).where(User.email == email)).first()

def find_user_by_username(session, user_name):
    return session.exec(select(User).where(User.user_name == user_name)).first()

def get_task_by_id(session: Session, task_id: int):
    task = session.exec(select(TaskReminder).where(TaskReminder.id == task_id)).first()
    return task if task else None

def delete_task_by_id(session: Session, task_id: int):
    task = session.exec(select(TaskReminder).where(TaskReminder.id == task_id)).first()
    if not task:
        return {"error": "Task not found"}

    session.exec(delete(TaskReminder).where(TaskReminder.id == task_id))
    session.commit()
    return {"message": "Task deleted successfully"}


def get_all_tasks(session: Session, user_name: str):
    return session.exec(select(TaskReminder).where(TaskReminder.assignee == user_name)).all()