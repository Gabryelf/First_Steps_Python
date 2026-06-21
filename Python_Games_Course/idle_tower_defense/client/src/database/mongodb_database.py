from typing import Dict, Any, Optional, List
from client.src.database.base_database import BaseDatabase
from client.src.utils.logger import logger

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, PyMongoError

    MONGO_AVAILABLE = True
except ImportError:
    MONGO_AVAILABLE = False
    logger.warning("PyMongo not available. Install with: pip install pymongo")


class MongoDBDatabase(BaseDatabase):
    """Реализация базы данных для MongoDB"""

    def __init__(self, connection_string: str = "mongodb://localhost:27017/",
                 database_name: str = "idle_tower_defense"):
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None
        self.db = None
        self.players_collection = None
        self.connected = False

        logger.info(f"MongoDBDatabase initialized for {database_name}")

    def connect(self) -> bool:
        """Подключение к MongoDB"""
        if not MONGO_AVAILABLE:
            logger.error("PyMongo not installed. Cannot connect to MongoDB")
            return False

        try:
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            # Проверка подключения
            self.client.admin.command('ping')
            self.db = self.client[self.database_name]
            self.players_collection = self.db['players']
            self.connected = True

            logger.info("Successfully connected to MongoDB")
            return True

        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            self.connected = False
            return False
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """Отключение от MongoDB"""
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("Disconnected from MongoDB")

    def save_player_data(self, player_id: str, data: Dict[str, Any]) -> bool:
        """Сохранение данных игрока"""
        if not self.connected or not self.players_collection:
            logger.error("Cannot save player data - not connected to MongoDB")
            return False

        try:
            result = self.players_collection.update_one(
                {'player_id': player_id},
                {'$set': data},
                upsert=True
            )
            logger.info(f"Player data saved for {player_id}")
            return result.acknowledged

        except PyMongoError as e:
            logger.error(f"Error saving player data: {e}")
            return False

    def load_player_data(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Загрузка данных игрока"""
        if not self.connected or not self.players_collection:
            logger.error("Cannot load player data - not connected to MongoDB")
            return None

        try:
            data = self.players_collection.find_one({'player_id': player_id})
            if data:
                # Удаляем _id из результата
                data.pop('_id', None)
                return data
            return None

        except PyMongoError as e:
            logger.error(f"Error loading player data: {e}")
            return None

    def update_player_stats(self, player_id: str, stats: Dict[str, Any]) -> bool:
        """Обновление статистики игрока"""
        if not self.connected or not self.players_collection:
            return False

        try:
            # Обновляем только статистику, не перезаписывая весь документ
            result = self.players_collection.update_one(
                {'player_id': player_id},
                {'$set': {f'stats.{k}': v for k, v in stats.items()}}
            )
            return result.acknowledged

        except PyMongoError as e:
            logger.error(f"Error updating player stats: {e}")
            return False

    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Получение таблицы лидеров"""
        if not self.connected or not self.players_collection:
            return []

        try:
            # Сортировка по high_score в убывающем порядке
            cursor = self.players_collection.find(
                {'high_score': {'$exists': True}}
            ).sort('high_score', -1).limit(limit)

            leaderboard = []
            for doc in cursor:
                leaderboard.append({
                    'player_id': doc['player_id'],
                    'high_score': doc.get('high_score', 0),
                    'level': doc.get('level', 1),
                    'player_name': doc.get('player_name', 'Unknown')
                })

            return leaderboard

        except PyMongoError as e:
            logger.error(f"Error getting leaderboard: {e}")
            return []