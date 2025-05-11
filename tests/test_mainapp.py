import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from taskserver.app import app
from taskserver.database import get_session
from taskserver.models import *
from .conftest import override_get_session

client = TestClient(app)

# Dependency override


app.dependency_overrides[get_session] = override_get_session

def test_dummy():
    response = client.get('/')
    assert response.status_code == 200
    assert 'TaskReminderServer' in response.json()