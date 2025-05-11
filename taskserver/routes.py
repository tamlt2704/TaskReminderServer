from fastapi import APIRouter

task_router = APIRouter()
user_router = APIRouter()


@task_router.get("/")
def get_tasks():
    return []


@user_router.get("/")
def get_users():
    return []