import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session, delete
from taskserver.app import app
from taskserver.database import get_session
from taskserver.models import *
from .conftest import override_get_session, test_engine

client = TestClient(app)

# Dependency override
app.dependency_overrides[get_session] = override_get_session

def test_create_user_should_work():
    response = client.post('api/v1/users', json={
        "name": "first_user",
        "email": "user@example.com",
        "password": "topsecretpassword"
    })
    assert response.status_code==200

def test_create_user_do_not_expore_more_than_expected():
    response = client.post('api/v1/users', json={
        "name": "second_user",
        "email": "second_user@example.com",
        "password": "topsecretpassword"
    })

    assert response.status_code==200
    # do not expose more than expected 
    js = response.json()
    print(js)
    assert len(js['user'].keys()) == 2
    assert 'name' in js['user'].keys() 
    assert 'email' in js['user'].keys()

def test_password_len_minimum():
    response = client.post('api/v1/users', json={
        "name": "first_user",
        "email": "user_with_invalid_password_len@example.com",
        "password": "123"
    })
    assert response.status_code==422

def test_duplicated_email_not_allowed():
    response = client.post('api/v1/users', json={
        "name": "first_user",
        "email": "dupemail@example.com",
        "password": "stringst"
    })
    assert response.status_code == 200

    response = client.post('api/v1/users', json={
        "name": "second_user",
        "email": "dupemail@example.com",
        "password": "stringst"
    })
    assert response.status_code==400