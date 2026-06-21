# server/src/services/user_service.py
import logging
from typing import Optional, List, Dict, Any
from ..models.user import User
from ..database.database import Database

logger = logging.getLogger(__name__)


class UserService:
    """Сервис для работы с пользователями"""

    def __init__(self, db: Database = None):
        self.db = db

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Получение пользователя по ID"""
        if not self.db:
            logger.error("Database not available")
            return None

        user_data = self.db.get_user_by_id(user_id)
        return User.from_db_row(user_data) if user_data else None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Получение пользователя по username"""
        if not self.db:
            logger.error("Database not available")
            return None

        user_data = self.db.get_user_by_username(username)
        return User.from_db_row(user_data) if user_data else None

    def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Обновление профиля пользователя"""
        if not self.db:
            logger.error("Database not available")
            return False

        # Разрешаем обновлять только определенные поля
        allowed_fields = ['display_name', 'avatar_url']
        update_fields = {k: v for k, v in profile_data.items() if k in allowed_fields}

        if not update_fields:
            logger.warning("No valid fields to update")
            return False

        set_clause = ", ".join([f"{field} = %s" for field in update_fields.keys()])
        query = f"UPDATE users SET {set_clause} WHERE id = %s"
        params = list(update_fields.values()) + [user_id]

        return self.db.execute_update(query, tuple(params))

    def get_user_stats(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Получение статистики пользователя"""
        if not self.db:
            logger.error("Database not available")
            return None

        # Получаем прогресс игрока
        progress_query = "SELECT * FROM player_progress WHERE user_id = %s"
        progress_data = self.db.execute_query(progress_query, (user_id,))

        # Получаем достижения
        achievements_query = """
        SELECT a.* FROM achievements a
        JOIN player_achievements pa ON a.id = pa.achievement_id
        WHERE pa.user_id = %s
        """
        achievements_data = self.db.execute_query(achievements_query, (user_id,))

        if not progress_data:
            return {
                "user_id": user_id,
                "highest_wave": 0,
                "total_enemies_defeated": 0,
                "total_coins_earned": 0,
                "games_played": 0,
                "games_won": 0,
                "achievements": achievements_data or []
            }

        progress = progress_data[0]
        return {
            "user_id": user_id,
            "highest_wave": progress.get('highest_wave', 0),
            "total_enemies_defeated": progress.get('total_enemies_defeated', 0),
            "total_coins_earned": progress.get('total_coins_earned', 0),
            "games_played": progress.get('games_played', 0),
            "games_won": progress.get('games_won', 0),
            "achievements": achievements_data or []
        }