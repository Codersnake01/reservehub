from pydantic import AnyUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    DATABASE_URL: AnyUrl = AnyUrl("postgresql+asyncpg://postgres@localhost:5434/reservehub")
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "dev-secret-change-me"

settings = Settings()