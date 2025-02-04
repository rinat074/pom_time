from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:password@localhost:5433/pomodoro-test"
    
    class Config:
        env_prefix = "TEST_" 