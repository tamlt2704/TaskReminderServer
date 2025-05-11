from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from .schemas import TaskReminderBase, ReminderType

class BaseEntity(SQLModel):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)    
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False, sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)})

class TaskReminder(BaseEntity, TaskReminderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    run_time: datetime
    assignee: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str
    modified_by: str
    reminder_type: ReminderType