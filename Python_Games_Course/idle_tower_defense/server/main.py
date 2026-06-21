# server/src/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

# Импорты API
from src.api.auth import router as auth_router
from src.api.users import router as users_router
from src.api.game import router as game_router
from src.api.social import router as social_router

# ✅ Используем SQLite
from src.database.sqlite_database import init_db, get_db
from src.core.config_sqlite import settings
from src.utils.logger import setup_logging

# Настройка логирования
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Idle Tower Defense Server with SQLite")

    success = await init_db()
    if success:
        logger.info("SQLite database initialized successfully")

        # Проверяем таблицы
        db = get_db()
        tables = db.execute_query("SELECT name FROM sqlite_master WHERE type='table'")
        if tables:
            logger.info(f"Database tables: {[table['name'] for table in tables]}")
    else:
        logger.error("Failed to initialize database")

    yield

    # Shutdown
    if get_db().is_connected:
        get_db().connection.close()
    logger.info("Server shut down")


app = FastAPI(
    title="Idle Tower Defense API",
    description="Backend server for Idle Tower Defense game",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(game_router, prefix="/api/v1/game", tags=["game"])
app.include_router(social_router, prefix="/api/v1/social", tags=["social"])


@app.get("/")
async def root():
    return {"message": "Idle Tower Defense Server is running with SQLite!"}


@app.get("/health")
async def health_check():
    db_status = "connected" if get_db().is_connected else "disconnected"
    return {
        "status": "healthy",
        "service": "idle-tower-defense-api",
        "database": db_status,
        "database_type": "SQLite"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
