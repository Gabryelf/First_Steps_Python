# server/src/core/config_dev.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 🖥️ ДЛЯ РАЗРАБОТКИ НА WINDOWS - localhost
    DATABASE_URL: str = "mysql+pymysql://root:rootpassword@localhost:3306/idle_tower_defense"

    JWT_SECRET: str = "idle-tower-defense-super-secret-key-2024-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7

    REDIS_URL: str = "redis://localhost:6379"

    DEBUG: bool = True
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000


settings = Settings()