from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_title: str = "Fast API Lessons"
    app_description: str = "Fast API Lessons"
    app_version: str = "0.0.1"
    GOOGLE_TOKEN_ID: str = "1234567890"
    sqlite_db_name: str = "pomodoro.sqlite"

settings = Settings()
