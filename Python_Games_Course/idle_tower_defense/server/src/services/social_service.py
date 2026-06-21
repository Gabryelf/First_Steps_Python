# server/src/services/social_service.py
import logging
from typing import Optional, Dict, Any, List
from ..database.database import Database

logger = logging.getLogger(__name__)


class SocialService:
    """Сервис для социальных функций"""

    def __init__(self, db: Database = None):
        self.db = db

    def get_player_visit_data(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Получение данных игрока для посещения"""
        if not self.db:
            logger.error("Database not available")
            return None

        try:
            # Базовая информация об игроке
            user_query = """
            SELECT u.id, u.username, u.display_name, u.avatar_url, u.level, u.experience
            FROM users u 
            WHERE u.id = %s AND u.is_active = TRUE
            """
            user_data = self.db.execute_query(user_query, (player_id,))

            if not user_data:
                return None

            user = user_data[0]

            # Прогресс игрока
            progress_query = "SELECT * FROM player_progress WHERE user_id = %s"
            progress_data = self.db.execute_query(progress_query, (player_id,))
            progress = progress_data[0] if progress_data else {}

            # Улучшения игрока
            upgrades_query = "SELECT upgrade_type, upgrade_level FROM player_upgrades WHERE user_id = %s"
            upgrades_data = self.db.execute_query(upgrades_query, (player_id,))
            upgrades = {row['upgrade_type']: row['upgrade_level'] for row in upgrades_data} if upgrades_data else {}

            # Достижения игрока
            achievements_query = """
            SELECT a.name, a.description, a.icon_url, pa.unlocked_at
            FROM achievements a
            JOIN player_achievements pa ON a.id = pa.achievement_id
            WHERE pa.user_id = %s
            ORDER BY pa.unlocked_at DESC
            LIMIT 10
            """
            achievements_data = self.db.execute_query(achievements_query, (player_id,))

            return {
                'player_info': {
                    'id': user['id'],
                    'username': user['username'],
                    'display_name': user['display_name'],
                    'avatar_url': user.get('avatar_url'),
                    'level': user.get('level', 1),
                    'experience': user.get('experience', 0)
                },
                'progress': {
                    'highest_wave': progress.get('highest_wave', 0),
                    'total_enemies_defeated': progress.get('total_enemies_defeated', 0),
                    'total_coins_earned': progress.get('total_coins_earned', 0),
                    'games_played': progress.get('games_played', 0),
                    'games_won': progress.get('games_won', 0)
                },
                'upgrades': upgrades,
                'recent_achievements': achievements_data or []
            }

        except Exception as e:
            logger.error(f"Failed to get player visit data: {e}")
            return None

    def add_friend(self, user_id: str, friend_username: str) -> bool:
        """Добавление в друзья"""
        if not self.db:
            logger.error("Database not available")
            return False

        try:
            # Находим ID друга по username
            friend_query = "SELECT id FROM users WHERE username = %s AND is_active = TRUE"
            friend_data = self.db.execute_query(friend_query, (friend_username,))

            if not friend_data:
                logger.warning(f"Friend not found: {friend_username}")
                return False

            friend_id = friend_data[0]['id']

            # Проверяем, не добавлен ли уже в друзья
            existing_query = """
            SELECT id FROM friends 
            WHERE (user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s)
            """
            existing = self.db.execute_query(existing_query, (user_id, friend_id, friend_id, user_id))

            if existing:
                logger.warning("Friendship already exists")
                return False

            # Добавляем запрос в друзья
            insert_query = "INSERT INTO friends (user_id, friend_id, status) VALUES (%s, %s, 'pending')"
            return self.db.execute_update(insert_query, (user_id, friend_id))

        except Exception as e:
            logger.error(f"Failed to add friend: {e}")
            return False

    def get_friends(self, user_id: str) -> List[Dict[str, Any]]:
        """Получение списка друзей"""
        if not self.db:
            logger.error("Database not available")
            return []

        try:
            query = """
            SELECT u.id, u.username, u.display_name, u.avatar_url, u.level, f.status, f.created_at
            FROM friends f
            JOIN users u ON (
                (f.user_id = %s AND f.friend_id = u.id) OR 
                (f.friend_id = %s AND f.user_id = u.id)
            )
            WHERE f.status = 'accepted' AND u.is_active = TRUE
            ORDER BY f.created_at DESC
            """
            result = self.db.execute_query(query, (user_id, user_id))
            return result or []

        except Exception as e:
            logger.error(f"Failed to get friends: {e}")
            return []