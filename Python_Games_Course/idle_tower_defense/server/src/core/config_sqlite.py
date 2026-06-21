# server/src/core/config_sqlite.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Используем SQLite для тестирования
    DATABASE_URL: str = "sqlite:///./data/test.db"

    JWT_SECRET: str = "idle-tower-defense-super-secret-key-2024-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7

    DEBUG: bool = True
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000


settings = Settings()