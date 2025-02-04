import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from tests.settings import TestSettings
from models import Base, UserProfile, Tasks, Categories

settings = TestSettings()

test_engine = create_async_engine(
    settings.db_url,
    future=True,
    echo=True,
)

async_session_maker = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

@pytest_asyncio.fixture(scope="session")
async def db_engine():
    # Добавим отладочный вывод
    print("\nCreating database tables...")
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully")
    yield test_engine
    print("\nDropping database tables...")
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("Tables dropped successfully")

@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    async with async_session_maker() as session:
        yield session
        # Очищаем данные после каждого теста
        async with session.begin():
            # Сначала очищаем таблицы с внешними ключами
            await session.execute(text('TRUNCATE TABLE "Tasks" CASCADE'))
            await session.execute(text('TRUNCATE TABLE "Categories" CASCADE'))
            await session.execute(text('TRUNCATE TABLE "UserProfile" CASCADE'))
        await session.commit() 