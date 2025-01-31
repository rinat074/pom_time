from exception import TaskNotFoundError
from repository import TaskRepository, CacheTask
from schema.task import Task, TaskCreateSchema
from dataclasses import dataclass

@dataclass
class TaskService:
    task_repository: TaskRepository
    cache_task: CacheTask

    async def get_tasks(self, user_id: int) -> list[Task]:
        if tasks := await self.cache_task.get_tasks(user_id):
            return tasks
        else:
            tasks = self.task_repository.get_tasks(user_id)
            await self.cache_task.set_tasks(tasks)
            return tasks
        
    async def create_task(self, body: TaskCreateSchema, user_id: int) -> Task:
        task_id = await self.task_repository.create_task(body, user_id)
        task = await self.get_task(task_id)
        return task
    
    async def get_task(self, task_id: int) -> Task:
        task = await self.task_repository.get_task(task_id)
        return Task.model_validate(task)
    
    async def update_task_name(self, task_id: int, name: str, user_id: int) -> Task:
        task = await self.task_repository.get_user_task(user_id, task_id)
        if not task:
            raise TaskNotFoundError
        task.name = name
        new_task = await self.task_repository.update_task(task)
        return Task.model_validate(new_task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self.task_repository.get_user_task(user_id, task_id)
        if not task:
            raise TaskNotFoundError
        await self.task_repository.delete_task(task_id)