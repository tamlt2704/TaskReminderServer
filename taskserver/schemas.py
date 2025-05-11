from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import datetime, date
from enum import Enum

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
        if scheduled_at.date() < date.today():
            raise ValueError("Scheduled should not be a past date")
        return scheduled_at

class TaskUpdate(TaskReminderBase):
    scheduled_at: datetime | None = None
    assignee: str | None = None
    content: str | None
    reminder_type: ReminderType | None

class TaskReminderCreate(TaskReminderBase):
    pass

class TaskReminderRead(TaskReminderCreate):
    id: int
    created_at: datetime
    updated_at: datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserRead(UserBase):
    pass

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class Token(BaseModel):
    access_token: str
    token_type: str