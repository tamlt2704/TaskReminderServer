
from sqlmodel import Session, select

from taskserver.schemas import TaskReminderCreate, UserBase
from taskserver.models import TaskReminder, User


def create_task_reminder(session: Session, data: TaskReminderCreate):
    reminder = TaskReminder.model_validate(data)
    session.add(reminder)
    session.commit()
    session.refresh(reminder)
    # user_pydantic = UserCreate(**user_db.dict(exclude={"id"}))  # Convert to Pydantic format
    # print(user_pydantic)
    return reminder

def save_user(session: Session, user_data: UserBase):
    user = User.model_validate(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def find_user_by_email_pattern(session: Session, email_pattern: str):
    users = session.exec(select(User).where(User.email.like(f"%{email_pattern}%"))).all()
    return users if users else {"error": "No users found"}