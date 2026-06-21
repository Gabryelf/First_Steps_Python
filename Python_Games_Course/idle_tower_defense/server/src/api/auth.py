# server/src/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional

from ..database.sqlite_database import get_db
from ..services.auth_service import AuthService
from ..models.user import User

router = APIRouter()
security = HTTPBearer()


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    display_name: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest, db=Depends(get_db)):
    auth_service = AuthService(db)

    # Проверяем существование пользователя
    if auth_service.get_user_by_username(request.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    if auth_service.get_user_by_email(request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Создаем пользователя
    user = auth_service.create_user(
        username=request.username,
        email=request.email,
        password=request.password,
        display_name=request.display_name or request.username
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

    # Создаем токен
    token = auth_service.create_access_token(user.id)

    return AuthResponse(
        access_token=token,
        expires_in=3600,  # 1 hour
        user=user.to_dict()
    )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db=Depends(get_db)):
    auth_service = AuthService(db)

    user = auth_service.authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Обновляем последний логин
    auth_service.update_last_login(user.id)

    # Создаем токен
    token = auth_service.create_access_token(user.id)

    return AuthResponse(
        access_token=token,
        expires_in=3600,
        user=user.to_dict()
    )


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db=Depends(get_db)
) -> User:
    auth_service = AuthService(db)

    user_id = auth_service.verify_token(credentials.credentials)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user