from sqlmodel import Session, select
from .models import Task, User

class TaskDao:
    def __init__(self, engine):
        self.engine = engine

    def get_session(self):
        with Session(self.engine) as session:
            return session

    def get_all_tasks(self):
        with self.get_session() as session:
            statement = select(Task)
            results = session.exec(statement)
            return results

    def save_user(self, user: User):
        with self.get_session() as session:
            session.add(user)
            session.commit()
            session.refresh(user)        
            return user
    
    def find_user_by_id(self, user_id: int):
        with self.get_session() as session:
            user = session.get(User, user_id)
            return user
    
    def save_task(self, task: Task):
        with self.get_session() as session:
            session.add(task)
            session.commit()
            session.refresh(task)
            return task
        
class UserDao:
    def __init__(self, engine):
        self.engine = engine

    def get_session(self):
        with Session(self.engine) as session:
            return session

    def find_user(self, username: str):
        with self.get_session() as session:
            statement = select(User).where(User.username == username)
            results = session.exec(statement)
            return results.first()