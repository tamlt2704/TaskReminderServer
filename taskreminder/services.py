class TaskService:
    def __init__(self, dao):
        self.dao = dao

    def creat_task(self):
        pass
    
    def get_all_tasks(self):
        return self.dao.get_all_tasks()