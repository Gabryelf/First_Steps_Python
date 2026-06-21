import jwt
from datetime import datetime, timedelta
from typing import Optional
import bcrypt
import logging
from ..models.user import User

logger = logging.getLogger(__name__)


class AuthService:
    """Сервис для аутентификации и авторизации"""

    def __init__(self, db):
        self.db = db
        logger.info("AuthService initialized")

    def hash_password(self, password: str) -> str:
        """Хеширование пароля"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверка пароля"""
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            logger.error(f"Password verification failed: {e}")
            return False

    def create_access_token(self, user_id: str) -> str:
        """Создание JWT токена"""
        expiration = datetime.utcnow() + timedelta(minutes=60)  # временно
        payload = {
            "sub": str(user_id),
            "exp": expiration,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        return jwt.encode(payload, "temp_secret", algorithm="HS256")  # временно

    def verify_token(self, token: str) -> Optional[str]:
        """Верификация JWT токена"""
        try:
            payload = jwt.decode(token, "temp_secret", algorithms=["HS256"])
            return payload.get("sub")
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Получение пользователя по ID"""
        logger.info(f"Getting user by ID: {user_id}")
        user_data = self.db.get_user_by_id(user_id)
        logger.info(f"User data from DB: {user_data}")
        return User.from_db_row(user_data) if user_data else None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Получение пользователя по username"""
        logger.info(f"Getting user by username: {username}")
        user_data = self.db.get_user_by_username(username)
        logger.info(f"User data from DB: {user_data}")
        return User.from_db_row(user_data) if user_data else None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Получение пользователя по email"""
        logger.info(f"Getting user by email: {email}")
        user_data = self.db.get_user_by_email(email)
        logger.info(f"User data from DB: {user_data}")
        return User.from_db_row(user_data) if user_data else None

    def create_user(self, username: str, email: str, password: str, display_name: str = None) -> Optional[User]:
        """Создание нового пользователя"""
        logger.info(f"Creating user: {username}, {email}")

        # Проверяем, не существует ли уже пользователь
        if self.get_user_by_username(username):
            logger.warning(f"Username already exists: {username}")
            return None
        if self.get_user_by_email(email):
            logger.warning(f"Email already exists: {email}")
            return None

        # Хешируем пароль
        password_hash = self.hash_password(password)
        logger.info("Password hashed successfully")

        # Создаем пользователя
        user_data = {
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.now().isoformat()
        }

        logger.info(f"Attempting to create user in DB with data: {user_data}")
        if self.db.create_user(user_data):
            logger.info("User created successfully in DB")
            # Получаем созданного пользователя
            return self.get_user_by_username(username)

        logger.error("Failed to create user in DB")
        return None

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Аутентификация пользователя"""
        user = self.get_user_by_username(username)
        if not user:
            return None

        if self.verify_password(password, user.password_hash):
            return user
        return None

    def update_last_login(self, user_id: str) -> bool:
        """Обновление времени последнего входа"""
        try:
            query = "UPDATE users SET last_login = ? WHERE id = ?"
            return self.db.execute_update(query, (datetime.now().isoformat(), user_id))
        except Exception as e:
            logger.error(f"Failed to update last login: {e}")
            return False