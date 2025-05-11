from sqlmodel import SQLModel, Field, UniqueConstraint
from datetime import datetime, timezone
from .schemas import TaskReminderBase, UserBase

class BaseEntity(SQLModel):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)    
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False, sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)})

class TaskReminder(BaseEntity, TaskReminderBase, table=True):
    pass

class User(BaseEntity, UserBase, table=True):
    hashed_password: str | None = None
    class Config:
        table_args = (UniqueConstraint("email", name="unique_email"),)