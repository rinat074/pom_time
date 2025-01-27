from fastapi import Depends
from sqlalchemy.orm import Session

from repository import TaskRepository, CacheTask, UserRepository
from service import TaskService, UserService, AuthService
from database import get_db_session
from cache import get_redis_connection

def get_tasks_repository(db_session: Session = Depends(get_db_session)) -> TaskRepository:
    return TaskRepository(db_session)

def get_cache_task() -> CacheTask:
    redis = get_redis_connection()
    return CacheTask(redis)

def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        cache_task: CacheTask = Depends(get_cache_task)
) -> TaskService:
    return TaskService(task_repository, cache_task)

def get_user_repository(db_session: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)

def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository=user_repository)

def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository=user_repository)