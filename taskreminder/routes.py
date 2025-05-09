from typing import Annotated
from fastapi import Depends
from taskreminder.app import app, task_service
from .auth import oauth2_scheme

@app.get("/tasks")
async def get_tasks(token: Annotated[str, Depends(oauth2_scheme)]):
    #return task_service.get_all_tasks()
    return {"token": token}

@app.post('/create_task')
def create_task(task_pojo):
    return task_service.creat_task(task_pojo)