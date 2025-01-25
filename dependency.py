from fastapi import Depends

from repository import TaskRepository, CacheTask
from service import TaskService
from database import get_db_session
from cache import get_redis_connection

def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)

def get_cache_task() -> CacheTask:
    redis = get_redis_connection()
    return CacheTask(redis)

def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        cache_task: CacheTask = Depends(get_cache_task)
) -> TaskService:
    return TaskService(task_repository, cache_task)
