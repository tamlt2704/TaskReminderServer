class TaskService:
    def __init__(self, dao):
        self.dao = dao

    def creat_task(self):
        pass
    
    def get_all_tasks(self):
        return self.dao.get_all_tasks()
    
class UserService:
    def __init__(self, dao):
        self.dao = dao

    def find_user(self, username):
        return self.dao.find_user(username)
    
    def create_user(self, user):
        return self.dao.create_user(user)