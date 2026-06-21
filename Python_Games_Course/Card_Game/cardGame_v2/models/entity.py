from abc import ABC, abstractmethod
from typing import List


class Entity(ABC):
    """Абстрактный базовый класс для всех существ в игре"""

    def __init__(self, name: str, max_health: int):
        self.name = name
        self._max_health = max_health
        self._current_health = max_health

    @property
    def current_health(self) -> int:
        return self._current_health

    @property
    def max_health(self) -> int:
        return self._max_health

    @property
    def is_alive(self) -> bool:
        return self._current_health > 0

    def take_damage(self, damage: int):
        """Нанесение урона существу"""
        self._current_health = max(0, self._current_health - damage)

    def heal(self, amount: int):
        """Лечение существа"""
        self._current_health = min(self._max_health, self._current_health + amount)

    @abstractmethod
    def get_available_actions(self) -> List[str]:
        """Получить доступные действия - абстрактный метод"""
        pass