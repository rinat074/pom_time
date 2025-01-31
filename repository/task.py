from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from schema import Task, TaskCreateSchema

from database import get_db_session
from models import Tasks, Categories

class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    async def get_tasks(self, user_id: int) -> list[Tasks]:
        async with self.session as session:
            tasks = (await session.execute(select(Tasks).where(Tasks.user_id == user_id))).scalars().all()
        return tasks
    
    async def get_task(self, id: int) -> Tasks | None:
        async with self.session as session:
            task = (await session.execute(select(Tasks).where(Tasks.id == id))).scalar_one_or_none()
        return task
    
    async def create_task(self, body: TaskCreateSchema, user_id: int) -> int:
        task_model = Tasks(
            name=body.name,
            pomodoro_count=body.pomodoro_count,
            category_id=body.category_id,
            user_id=user_id
        )
        async with self.session as session:
            session.add(task_model)
            await session.commit()
            return task_model.id
    
    async def update_task(self, task: Tasks) -> Tasks:
        async with self.session as session:
            session.merge(task)
            await session.commit()
        return task
    
    async def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        async with self.session as session:
            task_id: int = (await session.execute(query)).scalar_one()
            await session.commit()
            return self.get_task(task_id)

    
    async def delete_task(self, id: int) -> None:
        async with self.session as session:
            await session.execute(delete(Tasks).where(Tasks.id == id))
            await session.commit()

    async def get_tasks_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == category_name)
        async with self.session as session:
            tasks = (await session.execute(query)).scalars().all()
        return tasks

    async def get_user_task(self, user_id: int, task_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        async with self.session as session:
            task = (await session.execute(query)).scalar_one_or_none()
        return task
