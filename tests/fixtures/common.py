import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db_session
from repository.user import UserRepository
from service.user import UserService
from service.auth import AuthService

@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    gen = get_db_session()
    session = await gen.__anext__()
    try:
        yield session
    finally:
        await gen.aclose()

@pytest_asyncio.fixture
async def user_repository(db_session: AsyncSession):
    return UserRepository(db_session=db_session)

@pytest_asyncio.fixture
async def auth_service(user_repository: UserRepository):
    return AuthService(user_repository=user_repository)

@pytest_asyncio.fixture
async def user_service(user_repository: UserRepository, auth_service: AuthService):
    return UserService(user_repository=user_repository, auth_service=auth_service)