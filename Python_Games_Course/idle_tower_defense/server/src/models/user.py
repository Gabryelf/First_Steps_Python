from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class User:
    def __init__(self, id: str, username: str, email: str, password_hash: str,
                 created_at: str, last_login: Optional[str] = None,
                 is_active: bool = True):
        self.id = str(id)  # Гарантируем что id - строка
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.last_login = last_login
        self.is_active = is_active

    @classmethod
    def from_db_row(cls, row):
        """Создает пользователя из строки базы данных"""
        if not row:
            return None

        try:
            logger.info(f"Creating User from row: {row}")

            # Адаптируемся к разным структурам базы
            # База имеет структуру: id, username, email, password_hash, created_at, last_login, is_active
            return cls(
                id=str(row[0]),  # ID
                username=row[1],  # username
                email=row[2],  # email
                password_hash=row[3],  # password_hash
                created_at=row[4],  # created_at
                last_login=row[5] if len(row) > 5 else None,  # last_login
                is_active=bool(row[6]) if len(row) > 6 else True  # is_active
            )
        except Exception as e:
            logger.error(f"Error creating User from row {row}: {e}")
            return None

    def to_dict(self):
        """Преобразует пользователя в словарь"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "is_active": self.is_active
        }

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"