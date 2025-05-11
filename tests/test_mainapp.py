import pytest
from fastapi.testclient import TestClient
from taskserver.app import app

client = TestClient(app)

def test_dummy():
    response = client.get('/')
    assert response.status_code == 200
    assert 'TaskReminderServer' in response.json()