from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from schema.task import Task

from database import Tasks, Categories, get_db_session

class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_tasks(self) -> list[Tasks]:
        with self.session() as session:
            tasks = session.execute(select(Tasks)).scalars().all()
        return tasks
    
    def get_task(self, id: int) -> Tasks | None:
        with self.session() as session:
            task = session.execute(select(Tasks).where(Tasks.id == id)).scalar_one_or_none()
        return task
    
    def create_task(self, task: Task) -> int:
        task_model = Tasks(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id
        )
        with self.session() as session:
            session.add(task_model)
            session.commit()
            return task_model.id
    
    def update_task(self, task: Tasks) -> Tasks:
        with self.session() as session:
            session.merge(task)
            session.commit()
        return task
    
    def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        with self.session() as session:
            task_id: int = session.execute(query).scalar_one()
            session.commit()
            return self.get_task(task_id)

    
    def delete_task(self, id: int) -> None:
        with self.session() as session:
            session.execute(delete(Tasks).where(Tasks.id == id))
            session.commit()

    def get_tasks_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == category_name)
        with self.session() as session:
            tasks = session.execute(query).scalars().all()
        return tasks
