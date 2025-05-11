from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import datetime, date, timezone
from enum import Enum
from typing import Optional

class ReminderType(str, Enum):
    email = "email"
    slack = "slack"

class TaskReminderBase(BaseModel):
    scheduled_at: datetime
    assignee: str
    content: str = Field(min_length=5, max_length=50)
    created_by: str | None = None
    modified_by: str | None = None
    reminder_type: ReminderType = Field(default=ReminderType.email)

    @field_validator("scheduled_at")
    def validate_password(scheduled_at):
        if scheduled_at.date() < datetime.now(timezone.utc).date():
            raise ValueError("Scheduled should not be a past date")
        return scheduled_at

class TaskUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    assignee: Optional[str] = None
    content: Optional[str] = None
    reminder_type: Optional[ReminderType] = None

class TaskReminderCreate(BaseModel):
    scheduled_at: datetime
    assignee: str
    content: str = Field(min_length=5, max_length=50)
    reminder_type: ReminderType = Field(default=ReminderType.email)

class TaskReminderRead(TaskReminderCreate):
    id: int
    created_at: datetime
    updated_at: datetime


class UserBase(BaseModel):
    user_name: str
    email: EmailStr

class UserRead(UserBase):
    pass

class UserCreate(UserBase):
    password: str = Field(min_length=8)

    @field_validator("user_name")
    def validate_user_name(user_name):
        if not user_name:
            raise ValueError("User name can not be empty")
        return user_name

class Token(BaseModel):
    access_token: str
    token_type: str