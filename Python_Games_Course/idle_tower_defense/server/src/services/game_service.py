# server/src/services/game_service.py
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from ..database.database import Database

logger = logging.getLogger(__name__)


class GameService:
    """Сервис для игровой логики"""

    def __init__(self, db: Database = None):
        self.db = db

    def save_player_progress(self, user_id: str, game_data: Dict[str, Any]) -> bool:
        """Сохранение прогресса игрока"""
        if not self.db:
            logger.error("Database not available")
            return False

        try:
            # Сохраняем улучшения
            upgrades = game_data.get('upgrades', {})
            self._save_player_upgrades(user_id, upgrades)

            # Обновляем прогресс игрока
            progress_data = {
                'user_id': user_id,
                'highest_wave': max(
                    game_data.get('current_wave', 0),
                    self._get_current_highest_wave(user_id)
                ),
                'total_enemies_defeated': game_data.get('enemies_defeated', 0),
                'total_coins_earned': game_data.get('coins', 0),
                'games_played': 1,  # Увеличиваем при каждом сохранении
                'updated_at': datetime.now()
            }

            # Проверяем существование записи прогресса
            existing_query = "SELECT id FROM player_progress WHERE user_id = %s"
            existing = self.db.execute_query(existing_query, (user_id,))

            if existing:
                # Обновляем существующую запись
                update_query = """
                UPDATE player_progress 
                SET highest_wave = %s, total_enemies_defeated = %s, 
                    total_coins_earned = %s, games_played = games_played + 1,
                    updated_at = %s
                WHERE user_id = %s
                """
                params = (
                    progress_data['highest_wave'],
                    progress_data['total_enemies_defeated'],
                    progress_data['total_coins_earned'],
                    progress_data['updated_at'],
                    user_id
                )
            else:
                # Создаем новую запись
                update_query = """
                INSERT INTO player_progress 
                (user_id, highest_wave, total_enemies_defeated, total_coins_earned, games_played, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                params = (
                    user_id,
                    progress_data['highest_wave'],
                    progress_data['total_enemies_defeated'],
                    progress_data['total_coins_earned'],
                    progress_data['games_played'],
                    progress_data['updated_at']
                )

            success = self.db.execute_update(update_query, params)

            # Проверяем достижения
            if success:
                self._check_achievements(user_id, progress_data)

            return success

        except Exception as e:
            logger.error(f"Failed to save player progress: {e}")
            return False

    def _save_player_upgrades(self, user_id: str, upgrades: Dict[str, Any]) -> bool:
        """Сохранение улучшений игрока"""
        if not upgrades:
            return True

        success = True
        for upgrade_type, level in upgrades.items():
            # Проверяем существование улучшения
            check_query = "SELECT id FROM player_upgrades WHERE user_id = %s AND upgrade_type = %s"
            existing = self.db.execute_query(check_query, (user_id, upgrade_type))

            if existing:
                # Обновляем уровень
                update_query = "UPDATE player_upgrades SET upgrade_level = %s WHERE user_id = %s AND upgrade_type = %s"
                success = success and self.db.execute_update(update_query, (level, user_id, upgrade_type))
            else:
                # Создаем новую запись
                insert_query = "INSERT INTO player_upgrades (user_id, upgrade_type, upgrade_level) VALUES (%s, %s, %s)"
                success = success and self.db.execute_update(insert_query, (user_id, upgrade_type, level))

        return success

    def _get_current_highest_wave(self, user_id: str) -> int:
        """Получение текущего максимального уровня волны игрока"""
        if not self.db:
            return 0

        query = "SELECT highest_wave FROM player_progress WHERE user_id = %s"
        result = self.db.execute_query(query, (user_id,))
        return result[0].get('highest_wave', 0) if result else 0

    def load_player_progress(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Загрузка прогресса игрока"""
        if not self.db:
            logger.error("Database not available")
            return None

        try:
            # Загружаем базовые данные пользователя
            user_query = "SELECT coins, diamonds, level FROM users WHERE id = %s"
            user_data = self.db.execute_query(user_query, (user_id,))

            if not user_data:
                return None

            # Загружаем улучшения
            upgrades_query = "SELECT upgrade_type, upgrade_level FROM player_upgrades WHERE user_id = %s"
            upgrades_data = self.db.execute_query(upgrades_query, (user_id,))

            upgrades = {row['upgrade_type']: row['upgrade_level'] for row in upgrades_data} if upgrades_data else {}

            # Загружаем прогресс
            progress_query = "SELECT * FROM player_progress WHERE user_id = %s"
            progress_data = self.db.execute_query(progress_query, (user_id,))

            progress = progress_data[0] if progress_data else {}

            return {
                'coins': user_data[0].get('coins', 100),
                'diamonds': user_data[0].get('diamonds', 0),
                'level': user_data[0].get('level', 1),
                'upgrades': upgrades,
                'highest_wave': progress.get('highest_wave', 0),
                'total_enemies_defeated': progress.get('total_enemies_defeated', 0),
                'total_coins_earned': progress.get('total_coins_earned', 0)
            }

        except Exception as e:
            logger.error(f"Failed to load player progress: {e}")
            return None

    def get_leaderboard(self, category: str = "wave") -> List[Dict[str, Any]]:
        """Получение таблицы лидеров"""
        if not self.db:
            logger.error("Database not available")
            return []

        try:
            if category == "wave":
                query = """
                SELECT u.username, u.display_name, u.avatar_url, pp.highest_wave as score
                FROM player_progress pp
                JOIN users u ON pp.user_id = u.id
                WHERE u.is_active = TRUE
                ORDER BY pp.highest_wave DESC
                LIMIT 100
                """
            elif category == "enemies":
                query = """
                SELECT u.username, u.display_name, u.avatar_url, pp.total_enemies_defeated as score
                FROM player_progress pp
                JOIN users u ON pp.user_id = u.id
                WHERE u.is_active = TRUE
                ORDER BY pp.total_enemies_defeated DESC
                LIMIT 100
                """
            else:
                query = """
                SELECT u.username, u.display_name, u.avatar_url, pp.highest_wave as score
                FROM player_progress pp
                JOIN users u ON pp.user_id = u.id
                WHERE u.is_active = TRUE
                ORDER BY pp.highest_wave DESC
                LIMIT 100
                """

            result = self.db.execute_query(query)
            return result or []

        except Exception as e:
            logger.error(f"Failed to get leaderboard: {e}")
            return []

    def _check_achievements(self, user_id: str, progress_data: Dict[str, Any]):
        """Проверка и выдача достижений"""
        if not self.db:
            return

        try:
            # Получаем все возможные достижения
            achievements_query = "SELECT * FROM achievements"
            all_achievements = self.db.execute_query(achievements_query) or []

            # Получаем уже полученные достижения
            user_achievements_query = "SELECT achievement_id FROM player_achievements WHERE user_id = %s"
            user_achievements = self.db.execute_query(user_achievements_query, (user_id,)) or []
            user_achievement_ids = {row['achievement_id'] for row in user_achievements}

            for achievement in all_achievements:
                if achievement['id'] in user_achievement_ids:
                    continue

                # Проверяем условие достижения
                requirement_type = achievement['requirement_type']
                requirement_value = achievement['requirement_value']

                if requirement_type == 'wave' and progress_data['highest_wave'] >= requirement_value:
                    self._grant_achievement(user_id, achievement)
                elif requirement_type == 'enemies' and progress_data['total_enemies_defeated'] >= requirement_value:
                    self._grant_achievement(user_id, achievement)
                elif requirement_type == 'coins' and progress_data['total_coins_earned'] >= requirement_value:
                    self._grant_achievement(user_id, achievement)
                elif requirement_type == 'games_played' and progress_data['games_played'] >= requirement_value:
                    self._grant_achievement(user_id, achievement)

        except Exception as e:
            logger.error(f"Failed to check achievements: {e}")

    def _grant_achievement(self, user_id: str, achievement: Dict[str, Any]):
        """Выдача достижения игроку"""
        try:
            # Добавляем достижение
            insert_query = "INSERT INTO player_achievements (user_id, achievement_id) VALUES (%s, %s)"
            self.db.execute_update(insert_query, (user_id, achievement['id']))

            # Начисляем награду
            if achievement.get('reward_coins', 0) > 0:
                update_query = "UPDATE users SET coins = coins + %s WHERE id = %s"
                self.db.execute_update(update_query, (achievement['reward_coins'], user_id))

            if achievement.get('reward_diamonds', 0) > 0:
                update_query = "UPDATE users SET diamonds = diamonds + %s WHERE id = %s"
                self.db.execute_update(update_query, (achievement['reward_diamonds'], user_id))

            logger.info(f"Achievement granted: {achievement['name']} to user {user_id}")

        except Exception as e:
            logger.error(f"Failed to grant achievement: {e}")