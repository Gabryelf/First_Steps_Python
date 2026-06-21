from abc import ABC, abstractmethod
from typing import Tuple


class Unit(ABC):

    def __init__(self, name: str, x: int, y: int, health: int = 100):
        self.name = name
        self._x = x
        self._y = y
        self.health = health
        self.max_health = health

    @property
    def position(self) -> Tuple[int, int]:
        return (self._x, self._y)

    @abstractmethod
    def symbol(self) -> str:
        pass

    def move(self, dx: int, dy: int, game_map) -> bool:

        new_x, new_y = self._x + dx, self._y + dy

        # Проверяем границы карты и проходимость тайла
        target_tile = game_map.get_tile(new_x, new_y)
        if target_tile.is_passable:
            self._x = new_x
            self._y = new_y
            return True
        return False

    def __str__(self) -> str:
        return f"{self.name} at {self.position} HP: {self.health}/{self.max_health}"