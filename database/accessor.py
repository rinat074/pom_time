
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from settings import settings

engine = create_async_engine(url = settings.db_url, future=True, echo=True, pool_pre_ping=True)

async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session
