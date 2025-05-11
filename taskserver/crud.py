
from sqlmodel import Session

from taskserver.schemas import TaskReminderCreate
from taskserver.models import TaskReminder


def create_task_reminder(session: Session, data: TaskReminderCreate):
    reminder = TaskReminder.model_validate(data)
    session.add(reminder)
    session.commit()
    session.refresh(reminder)
    # user_pydantic = UserCreate(**user_db.dict(exclude={"id"}))  # Convert to Pydantic format
    # print(user_pydantic)
    return reminder