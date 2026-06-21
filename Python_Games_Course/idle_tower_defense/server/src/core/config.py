# server/src/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # 🐳 ДЛЯ DOCKER - используем имя сервиса как хост
    DATABASE_URL: str = "mysql+pymysql://root:rootpassword@mysql:3306/idle_tower_defense"

    # 🔐 JWT
    JWT_SECRET: str = "idle-tower-defense-super-secret-key-2024-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7

    # Redis
    REDIS_URL: str = "redis://redis:6379"

    # Настройки приложения
    DEBUG: bool = True
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()