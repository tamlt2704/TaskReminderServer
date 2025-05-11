import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from taskserver.app import app
from taskserver.database import get_session

client = TestClient(app)
# Set up a test database
test_engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(test_engine)
# Dependency override
def override_get_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

# Dependency override
def override_get_session():
    with Session(test_engine) as session:
        yield session

def test_dummy():
    response = client.get('/')
    assert response.status_code == 200
    assert 'TaskReminderServer' in response.json()