from fastapi import Depends, HTTPException, Security, security
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from exception import TokenExpiredError, TokenNotValidError
from repository import TaskRepository, CacheTask, UserRepository
from service import TaskService, UserService, AuthService
from database import get_db_session
from cache import get_redis_connection


async def get_tasks_repository(db_session: AsyncSession = Depends(get_db_session)) -> TaskRepository:
    return TaskRepository(db_session)

async def get_cache_task() -> CacheTask:
    redis = await get_redis_connection()
    return CacheTask(redis)

async def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        cache_task: CacheTask = Depends(get_cache_task)
) -> TaskService:
    return TaskService(task_repository, cache_task)

async def get_user_repository(db_session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)

async def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository=user_repository)

async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)

reusable_oauth2 = security.HTTPBearer()

async def get_request_user_id(
        request: Request,
        auth_service: AuthService = Depends(get_auth_service),
        token: security.HTTPAuthorizationCredentials = Security(reusable_oauth2)
        ) -> int:
    try:
        user_id = auth_service.get_user_id_from_token(token.credentials)
        return user_id
    except TokenExpiredError as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except TokenNotValidError as e:
        raise HTTPException(status_code=401, detail=e.detail)