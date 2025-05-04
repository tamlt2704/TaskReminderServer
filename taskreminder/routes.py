from taskreminder.app import app, task_service

@app.get("/")
async def main_route():
    return {"message": "Hello world"}

@app.get("/tasks")
def get_tasks():
    return task_service.get_all_tasks()


@app.post('/create_task')
def create_task(task_pojo):
    return task_service.creat_task(task_pojo)