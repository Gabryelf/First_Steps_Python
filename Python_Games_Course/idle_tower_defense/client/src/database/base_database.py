from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from client.src.utils.logger import logger


class BaseDatabase(ABC):
    """Абстрактный базовый класс для работы с базой данных"""

    @abstractmethod
    def connect(self) -> bool:
        """Подключение к базе данных"""
        pass

    @abstractmethod
    def disconnect(self):
        """Отключение от базы данных"""
        pass

    @abstractmethod
    def save_player_data(self, player_id: str, data: Dict[str, Any]) -> bool:
        """Сохранение данных игрока"""
        pass

    @abstractmethod
    def load_player_data(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Загрузка данных игрока"""
        pass

    @abstractmethod
    def update_player_stats(self, player_id: str, stats: Dict[str, Any]) -> bool:
        """Обновление статистики игрока"""
        pass

    @abstractmethod
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Получение таблицы лидеров"""
        pass


class MockDatabase(BaseDatabase):
    """Заглушка базы данных для разработки"""

    def __init__(self):
        self._data = {}
        self.connected = False
        logger.info("MockDatabase initialized")

    def connect(self) -> bool:
        self.connected = True
        logger.info("MockDatabase connected")
        return True

    def disconnect(self):
        self.connected = False
        logger.info("MockDatabase disconnected")

    def save_player_data(self, player_id: str, data: Dict[str, Any]) -> bool:
        if not self.connected:
            return False

        self._data[player_id] = data
        logger.info(f"Player data saved for {player_id}")
        return True

    def load_player_data(self, player_id: str) -> Optional[Dict[str, Any]]:
        if not self.connected:
            return None

        return self._data.get(player_id)

    def update_player_stats(self, player_id: str, stats: Dict[str, Any]) -> bool:
        if not self.connected:
            return False

        if player_id not in self._data:
            self._data[player_id] = {}

        self._data[player_id].update(stats)
        logger.info(f"Player stats updated for {player_id}")
        return True

    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        if not self.connected:
            return []

        # Простая реализация лидерборда
        players = []
        for player_id, data in self._data.items():
            if 'high_score' in data:
                players.append({
                    'player_id': player_id,
                    'high_score': data['high_score'],
                    'level': data.get('level', 1)
                })

        # Сортировка по убыванию счета
        players.sort(key=lambda x: x['high_score'], reverse=True)
        return players[:limit]