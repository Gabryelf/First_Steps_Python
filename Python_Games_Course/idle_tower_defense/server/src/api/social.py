# server/src/api/social.py
from fastapi import APIRouter, Depends

from ..services.social_service import SocialService
from ..models.user import User
from .auth import get_current_user

router = APIRouter()

@router.get("/visit/{player_id}")
async def visit_player(
    player_id: str,
    current_user: User = Depends(get_current_user)
):
    """Посещение другого игрока"""
    social_service = SocialService()
    player_data = social_service.get_player_visit_data(player_id)
    if not player_data:
        return {"error": "Player not found"}
    return player_data