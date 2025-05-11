import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from taskserver.app import app
from taskserver.database import get_session
from taskserver.models import *
from .conftest import override_get_session
from taskserver.auth import get_current_active_user
client = TestClient(app)

# Dependency override

def override_active_user():
    yield None#User(user_name="tom", email="tom@example.com")

app.dependency_overrides[get_session] = override_get_session
app.dependency_overrides[get_current_active_user] = override_active_user



def ensure_user_exist():
    client.post('api/v1/users', json={
        "user_name": "tom",
        "email": "tom@example.com",
        "password": "topsecretpassword"
    })

    client.post('api/v1/users', json={
        "user_name": "jerry",
        "email": "jerry@example.com",
        "password": "topsecretpassword"
    })

    client.post('api/v1/users', json={
        "user_name": "pikachu",
        "email": "pikachu@example.com",
        "password": "topsecretpassword"
    })

    response = client.get('api/v1/users/search/example.com')
    assert response.status_code == 200
    assert response.json() == [{'user_name': 'tom', 'email': 'tom@example.com'}, {'user_name': 'jerry', 'email': 'jerry@example.com'}, {'user_name': 'pikachu', 'email': 'pikachu@example.com'}]

def test_creat_task_should_work():
    ensure_user_exist()
    response = client.post('/api/v1/tasks', json={
        "scheduled_at": datetime.now(timezone.utc).isoformat(),
        "assignee": "tom",
        "content": "string",        
        "reminder_type": "email"
    })
    assert response.status_code == 200

    assert response.json()['created_by'] == 'tom'
    assert response.json()['reminder_type'] == 'email'

def test_asssignee_should_exist():
    ensure_user_exist()

    response = client.post('/api/v1/tasks', json={
        "scheduled_at": datetime.now(timezone.utc).isoformat(),
        "assignee": "thisuserdoesnotexist",
        "content": "string",        
        "reminder_type": "email"
    })
    assert response.status_code == 400
    assert response.json() == {'detail': 'User name thisuserdoesnotexist does not exist'}