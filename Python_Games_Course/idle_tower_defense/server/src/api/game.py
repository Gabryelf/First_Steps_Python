# server/src/api/game.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict, Any

from ..services.game_service import GameService
from ..models.user import User
from .auth import get_current_user

router = APIRouter()

class SaveProgressRequest(BaseModel):
    coins: int
    diamonds: int
    score: int
    current_wave: int
    enemies_defeated: int
    upgrades: Dict[str, Any]

@router.post("/save-progress")
async def save_game_progress(
    request: SaveProgressRequest,
    current_user: User = Depends(get_current_user)
):
    """Сохранение прогресса игры"""
    game_service = GameService()
    success = game_service.save_player_progress(current_user.id, request.dict())
    return {"success": success}

@router.get("/load-progress")
async def load_game_progress(current_user: User = Depends(get_current_user)):
    """Загрузка прогресса игры"""
    game_service = GameService()
    progress = game_service.load_player_progress(current_user.id)
    return progress or {}

@router.get("/leaderboard")
async def get_leaderboard(category: str = "wave"):
    """Получение таблицы лидеров"""
    game_service = GameService()
    leaderboard = game_service.get_leaderboard(category)
    return leaderboard