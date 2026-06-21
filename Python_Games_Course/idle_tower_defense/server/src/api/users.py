# server/src/api/users.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from ..services.user_service import UserService
from ..models.user import User
from .auth import get_current_user

router = APIRouter()

@router.get("/me", response_model=dict)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Получение информации о текущем пользователе"""
    return current_user.to_dict()

@router.get("/{user_id}", response_model=dict)
async def get_user_info(user_id: str, db=Depends(get_current_user)):
    """Получение информации о пользователе по ID"""
    user_service = UserService()
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_dict()