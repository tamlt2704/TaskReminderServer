from taskreminder.models import Task, User, ReminderType
from taskreminder.dao import TaskDao
from taskreminder.db import engine
from sqlmodel import SQLModel
from datetime import datetime, timedelta

SQLModel.metadata.create_all(engine)
task_dao = TaskDao(engine)
 
def test_dummy():
    assert 1 + 1 == 2

def test_save_user():
    user = User(name="test_user")
    saved_user = task_dao.save_user(user)
    assert saved_user.id is not None
    db_user = task_dao.find_user_by_id(saved_user.id)
    assert db_user.name == "test_user"
 
def test_save_task():
    user = User(name="test_user")
    saved_user = task_dao.save_user(user)
    task = Task(content="test_task",
                scheduled_at=datetime.now() + timedelta(days=1),
                created_by=saved_user.id,
                modified_by=saved_user.id,
                assigned_to=saved_user.id,
                reminder_type=ReminderType.EMAIL
                )
    saved_task = task_dao.save_task(task)
    assert saved_task.id is not None
    assert saved_task.created_by == saved_user.id
 
    print("---------------DEBUG 1", saved_task)
 
    print("DEBUG update")
    saved_task.content = "test_task_updated"
    saved_task = task_dao.save_task(saved_task)
    assert saved_task.content == "test_task_updated"
 
    print("--------------DEBUG 2", saved_task)
 