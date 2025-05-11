from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from .schemas import TaskReminderBase, ReminderType

class BaseEntity(SQLModel):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)    
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False, sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)})

class TaskReminder(BaseEntity, TaskReminderBase, table=True):
    pass