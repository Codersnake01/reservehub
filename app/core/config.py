from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    DATABASE_URL: AnyUrl = AnyUrl(
        "postgresql+asyncpg://postgres@localhost:5434/reservehub"
    )
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "dev-secret-change-me"

    # Email
    EMAIL_HOST: str = "mailpit"
    EMAIL_PORT: int = 1025
    EMAIL_USE_TLS: bool = False
    RESEND_API_KEY: str | None = None  # Solo se usa en producción


settings = Settings()
