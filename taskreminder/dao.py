from sqlmodel import Session, select
from .models import Task 

class TaskDao:
    def __init__(self, engine):
        self.engine = engine

    def get_all_tasks(self):
        with Session(self.engine) as session:
            statement = select(Task)
            results = session.exec(statement)
            return results

    