from repository import TaskRepository, CacheTask
from schema.task import Task
from dataclasses import dataclass

@dataclass
class TaskService:
    task_repository: TaskRepository
    cache_task: CacheTask

    def get_tasks(self) -> list[Task]:
        if tasks := self.cache_task.get_tasks():
            return tasks
        else:
            tasks = self.task_repository.get_tasks()
            self.cache_task.set_tasks(tasks)
            return tasks
