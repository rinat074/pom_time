from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from schema import Task, TaskCreateSchema

from database import get_db_session
from models import Tasks, Categories

class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_tasks(self, user_id: int) -> list[Tasks]:
        with self.session() as session:
            tasks = session.execute(select(Tasks).where(Tasks.user_id == user_id)).scalars().all()
        return tasks
    
    def get_task(self, id: int) -> Tasks | None:
        with self.session() as session:
            task = session.execute(select(Tasks).where(Tasks.id == id)).scalar_one_or_none()
        return task
    
    def create_task(self, body: TaskCreateSchema, user_id: int) -> int:
        task_model = Tasks(
            name=body.name,
            pomodoro_count=body.pomodoro_count,
            category_id=body.category_id,
            user_id=user_id
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

    def get_user_task(self, user_id: int, task_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        with self.session() as session:
            task = session.execute(query).scalar_one_or_none()
        return task
