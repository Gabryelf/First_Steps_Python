# server/src/database/sqlite_database.py
import sqlite3
import os
import logging
from typing import Optional, Dict, Any, List
import uuid

logger = logging.getLogger(__name__)


class SQLiteDatabase:
    def __init__(self):
        self.connection = None
        self.is_connected = False
        self.db_path = "data/test.db"

    async def connect(self) -> bool:
        """Подключение к SQLite базе"""
        try:
            # Создаем папку для данных
            os.makedirs("data", exist_ok=True)

            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self.is_connected = True

            # Создаем таблицы
            self._create_tables()

            logger.info(f"✅ SQLite database connected: {self.db_path}")
            return True

        except Exception as e:
            logger.error(f"❌ SQLite connection failed: {e}")
            return False

    def _create_tables(self):
        """Создание необходимых таблиц"""
        tables = [
            # Пользователи
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                display_name TEXT,
                avatar_url TEXT,
                experience INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                coins INTEGER DEFAULT 100,
                diamonds INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL,
                is_active BOOLEAN DEFAULT 1
            )
            """,
            # Прогресс игроков
            """
            CREATE TABLE IF NOT EXISTS player_progress (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                highest_wave INTEGER DEFAULT 0,
                total_enemies_defeated INTEGER DEFAULT 0,
                total_coins_earned INTEGER DEFAULT 0,
                total_play_time INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0,
                games_won INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(user_id)
            )
            """,
            # Улучшения игроков
            """
            CREATE TABLE IF NOT EXISTS player_upgrades (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                upgrade_type TEXT NOT NULL,
                upgrade_level INTEGER DEFAULT 1,
                purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(user_id, upgrade_type)
            )
            """,
            # Достижения
            """
            CREATE TABLE IF NOT EXISTS achievements (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                icon_url TEXT,
                requirement_type TEXT NOT NULL,
                requirement_value INTEGER NOT NULL,
                reward_coins INTEGER DEFAULT 0,
                reward_diamonds INTEGER DEFAULT 0
            )
            """,
            # Полученные достижения
            """
            CREATE TABLE IF NOT EXISTS player_achievements (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                achievement_id TEXT NOT NULL,
                unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE,
                UNIQUE(user_id, achievement_id)
            )
            """
        ]

        with self.connection:
            for table_sql in tables:
                self.connection.execute(table_sql)

        # Добавляем тестовые достижения
        self._seed_achievements()

        logger.info("SQLite tables created")

    def _seed_achievements(self):
        """Добавление тестовых достижений"""
        achievements = [
            ("first_steps", "First Steps", "Complete wave 5", "wave", 5, 100, 1),
            ("tower_defender", "Tower Defender", "Complete wave 10", "wave", 10, 250, 2),
            ("enemy_slayer", "Enemy Slayer", "Defeat 100 enemies", "enemies", 100, 150, 1),
            ("wealthy_defender", "Wealthy Defender", "Earn 1000 coins", "coins", 1000, 200, 2),
            ("veteran", "Veteran", "Play 10 games", "games_played", 10, 300, 3)
        ]

        # Проверяем есть ли уже достижения
        cursor = self.connection.execute("SELECT COUNT(*) as count FROM achievements")
        count = cursor.fetchone()["count"]

        if count == 0:
            for achievement_id, name, desc, req_type, req_value, coins, diamonds in achievements:
                self.connection.execute(
                    "INSERT INTO achievements (id, name, description, requirement_type, requirement_value, reward_coins, reward_diamonds) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (achievement_id, name, desc, req_type, req_value, coins, diamonds)
                )
            self.connection.commit()
            logger.info("Test achievements added")

    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict[str, Any]]]:
        if not self.is_connected:
            logger.error("Database not connected")
            return None

        try:
            cursor = self.connection.execute(query, params or ())
            results = cursor.fetchall()
            return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return None

    def execute_update(self, query: str, params: tuple = None) -> bool:
        if not self.is_connected:
            logger.error("Database not connected")
            return False

        try:
            self.connection.execute(query, params or ())
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Update failed: {e}")
            return False

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        result = self.execute_query("SELECT * FROM users WHERE id = ? AND is_active = 1", (user_id,))
        return result[0] if result else None

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        result = self.execute_query("SELECT * FROM users WHERE username = ? AND is_active = 1", (username,))
        return result[0] if result else None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        result = self.execute_query("SELECT * FROM users WHERE email = ? AND is_active = 1", (email,))
        return result[0] if result else None

    def create_user(self, user_data: Dict[str, Any]) -> bool:
        query = """
        INSERT INTO users (id, username, email, password_hash, display_name, avatar_url)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            str(uuid.uuid4()),
            user_data['username'],
            user_data['email'],
            user_data['password_hash'],
            user_data.get('display_name', user_data['username']),
            user_data.get('avatar_url')
        )
        return self.execute_update(query, params)


# Глобальный экземпляр
sqlite_db = SQLiteDatabase()


async def init_db():
    return await sqlite_db.connect()


def get_db():
    return sqlite_db