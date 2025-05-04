from sqlmodel import Field, SQLModel, Enum, Column
from datetime import datetime, timezone

class ReminderType(str, Enum):
    EMAIL = "email"
    SLACK = "slack"

class BaseEntity(SQLModel):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )

class User(BaseEntity, table=True):
    name: str

class Task(BaseEntity, table=True):
    time_to_run: datetime
    user_id: int = Field(default=None, foreign_key="user.id") # who should perform the reminder
    content: str
    creator: int = Field(default=None, foreign_key="user.id")
    modifier: int = Field(default=None, foreign_key="user.id")
    reminder_type: Field(sa_column=Column(Enum(ReminderType)))