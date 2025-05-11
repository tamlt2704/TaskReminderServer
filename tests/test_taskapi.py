import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from taskserver.app import app
from taskserver.database import get_session
from taskserver.models import *
from .conftest import override_get_session
from taskserver.auth import get_current_active_user
client = TestClient(app)

test_current_active_user = User(user_name="tom", email="tom@example.com")
def override_active_user():
    yield test_current_active_user

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


def create_a_valid_task(assignee, content="default task"):
    return client.post('/api/v1/tasks', json={
        "scheduled_at": datetime.now(timezone.utc).isoformat(),
        "assignee": assignee,
        "content": content,
        "reminder_type": "email"
    })

def test_creat_task_should_work():
    ensure_user_exist()
    
    response = create_a_valid_task(assignee='jerry')
    assert response.status_code == 200

    assert response.json()['created_by'] == 'tom'
    assert response.json()['reminder_type'] == 'email'

def test_creat_task_creator_is_current_active_user():
    ensure_user_exist()
    
    response = create_a_valid_task(assignee='jerry', content='default')
    assert response.status_code == 200

    assert response.json()['created_by'] == test_current_active_user.user_name
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

def test_conten_is_required():
    ensure_user_exist()

    response = client.post('/api/v1/tasks', json={
        "scheduled_at": datetime.now(timezone.utc).isoformat(),
        "assignee": "thisuserdoesnotexist",
        "content": "",        
        "reminder_type": "email"
    })
    assert response.status_code == 422

def test_get_task_by_id_should_work():
    ensure_user_exist()

    response = create_a_valid_task(assignee='jerry', content='default')
    assert response.status_code == 200
    
    response = client.get(f"/api/v1/tasks/{response.json()['id']}")
    assert response.status_code == 200
    assert response.json()['created_by'] == test_current_active_user.user_name
    assert response.json()['assignee'] == 'jerry'

def test_update_should_work():
    ensure_user_exist()

    response = create_a_valid_task(assignee='jerry', content='default')
    assert response.status_code == 200
    
    task_id = response.json()['id']
    response = client.put(f"/api/v1/tasks/{task_id}", json={
        'assignee': 'pikachu'
    })
    assert response.status_code == 200
    assert response.json()['created_by'] == test_current_active_user.user_name
    assert response.json()['modified_by'] == test_current_active_user.user_name
    assert response.json()['assignee'] == 'pikachu'

def test_get_task_for_user_should_work():
    ensure_user_exist()

    response = create_a_valid_task(assignee='jerry', content='default')
    assert response.status_code == 200
    
    response = client.get(f"/api/v1/tasks/usertask/jerry")
    assert response.status_code == 200
    assert len(response.json()) > 0