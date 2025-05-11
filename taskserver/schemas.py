from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class ReminderType(str, Enum):
    email = "email"
    slack = "slack"

class TaskReminderBase(BaseModel):
    run_time: datetime
    assignee: str
    content: str
    created_by: str
    modified_by: str
    reminder_type: ReminderType

class TaskReminderCreate(TaskReminderBase):
    pass

class TaskReminderRead(TaskReminderCreate):
    id: int
    created_at: datetime
    updated_at: datetime