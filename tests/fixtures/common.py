import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from repository.user import UserRepository
from repository.task import TaskRepository
from service.user import UserService
from service.auth import AuthService
from service.task import TaskService

@pytest_asyncio.fixture(scope="function")
async def user_repository(db_session: AsyncSession):
    repo = UserRepository(db_session=db_session)
    yield repo

@pytest_asyncio.fixture(scope="function")
async def task_repository(db_session: AsyncSession):
    repo = TaskRepository(db_session=db_session)
    yield repo

@pytest_asyncio.fixture(scope="function")
async def auth_service(user_repository: UserRepository):
    service = AuthService(user_repository=user_repository)
    yield service

@pytest_asyncio.fixture(scope="function")
async def user_service(user_repository: UserRepository, auth_service: AuthService):
    service = UserService(user_repository=user_repository, auth_service=auth_service)
    yield service