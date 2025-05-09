from sqlmodel import Field, SQLModel, Column
from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel


class ReminderType(Enum):
    EMAIL = "Email"
    SLACK = "Slack"

class BaseEntity(SQLModel):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)    
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False, sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)})

class User(BaseEntity, table=True):
    username: str
    disabled: bool | None = None
    hashed_password: str

class Task(BaseEntity, table=True):
    content: str
    scheduled_at: datetime
    assigned_to: int = Field(default=None, foreign_key="user.id") # who should perform the reminder
    created_by: int = Field(default=None, foreign_key="user.id")
    modified_by: int = Field(default=None, foreign_key="user.id")
    reminder_type: ReminderType = Field(default=ReminderType.EMAIL)

class Token(BaseModel):
    access_token: str
    token_type: str