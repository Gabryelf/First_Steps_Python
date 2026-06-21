# server/src/database/database.py
import pymysql
from typing import Optional, Dict, Any, List
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)


class Database:
    """Класс для работы с MySQL базой данных"""

    def __init__(self):
        self.connection = None
        self.is_connected = False

    async def connect(self) -> bool:
        """Подключение к базе данных"""
        try:
            # Парсим URL базы данных
            # format: mysql+pymysql://user:password@host:port/database
            db_url = settings.DATABASE_URL
            if db_url.startswith('mysql+pymysql://'):
                db_url = db_url.replace('mysql+pymysql://', '')

            # Парсим параметры
            user_pass, host_port_db = db_url.split('@')
            user, password = user_pass.split(':')
            host_port, database = host_port_db.split('/')
            host, port = host_port.split(':') if ':' in host_port else (host_port, '3306')

            self.connection = pymysql.connect(
                host=host,
                port=int(port),
                user=user,
                password=password,
                database=database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

            self.is_connected = True
            logger.info("Successfully connected to MySQL database")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        """Отключение от базы данных"""
        if self.connection:
            self.connection.close()
            self.is_connected = False
            logger.info("Disconnected from database")

    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict[str, Any]]]:
        """Выполнение SELECT запроса"""
        if not self.is_connected:
            logger.error("Database not connected")
            return None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                result = cursor.fetchall()
                return result
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return None

    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Выполнение INSERT/UPDATE запроса"""
        if not self.is_connected:
            logger.error("Database not connected")
            return False

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
                return True
        except Exception as e:
            logger.error(f"Update execution failed: {e}")
            self.connection.rollback()
            return False

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Получение пользователя по ID"""
        query = "SELECT * FROM users WHERE id = %s AND is_active = TRUE"
        result = self.execute_query(query, (user_id,))
        return result[0] if result else None

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Получение пользователя по username"""
        query = "SELECT * FROM users WHERE username = %s AND is_active = TRUE"
        result = self.execute_query(query, (username,))
        return result[0] if result else None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Получение пользователя по email"""
        query = "SELECT * FROM users WHERE email = %s AND is_active = TRUE"
        result = self.execute_query(query, (email,))
        return result[0] if result else None

    def create_user(self, user_data: Dict[str, Any]) -> bool:
        """Создание нового пользователя"""
        query = """
        INSERT INTO users (username, email, password_hash, display_name, avatar_url)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            user_data['username'],
            user_data['email'],
            user_data['password_hash'],
            user_data.get('display_name', user_data['username']),
            user_data.get('avatar_url')
        )
        return self.execute_update(query, params)


# Глобальный экземпляр базы данных
db = Database()


async def init_db():
    """Инициализация базы данных"""
    return await db.connect()


def get_db():
    """Получение экземпляра базы данных для dependency injection"""
    return db