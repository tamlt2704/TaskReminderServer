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

def test_create_user_should_work(setup_function):
    response = client.post('api/v1/users', json={
        "user_name": "first_user",
        "email": "user@example.com",
        "password": "topsecretpassword"
    })
    assert response.status_code==200

def test_email_validation():
    response = client.post('api/v1/users', json={
        "user_name": "invalid",
        "email": "user@",
        "password": "topsecretpassword"
    })
    assert response.status_code==422


def test_user_name_can_not_empty():
    response = client.post('api/v1/users', json={
        "user_name": "",
        "email": "user@example.com",
        "password": "topsecretpassword"
    })
    assert response.status_code==422

def test_create_user_do_not_expore_more_than_expected():
    response = client.post('api/v1/users', json={
        "user_name": "second_user",
        "email": "second_user@example.com",
        "password": "topsecretpassword"
    })

    assert response.status_code==200
    # do not expose more than expected 
    js = response.json()
    print(js)
    assert len(js['user'].keys()) == 2
    assert 'user_name' in js['user'].keys() 
    assert 'email' in js['user'].keys()

def test_password_len_minimum():
    response = client.post('api/v1/users', json={
        "user_name": "first_user",
        "email": "user_with_invalid_password_len@example.com",
        "password": "123"
    })
    assert response.status_code==422

def test_duplicated_email_not_allowed():
    response = client.post('api/v1/users', json={
        "user_name": "third_user",
        "email": "third_user@example.com",
        "password": "stringst"
    })
    assert response.status_code == 200

    response = client.post('api/v1/users', json={
        "user_name": "third_user_again",
        "email": "third_user@example.com",
        "password": "stringst"
    })
    assert response.status_code==400

def test_search_user_should_work():
    response = client.post('api/v1/users', json={
        "user_name": "third_user",
        "email": "third_user@example.com",
        "password": "stringst"
    })
    assert response.status_code == 200

    response = client.get('api/v1/users/search/example.com')
    assert response.json() == [{'user_name': 'third_user', 'email': 'third_user@example.com'}]