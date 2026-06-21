from .entity import Entity
from typing import List
import random


class Enemy(Entity):
    """Класс врага"""

    def __init__(self, name: str, max_health: int, damage: int = 10):
        super().__init__(name, max_health)
        self.damage = damage

    def get_available_actions(self) -> List[str]:
        return ["атаковать"]

    def make_turn(self, target: Entity) -> str:
        """Враг делает ход"""
        if self.is_alive:
            target.take_damage(self.damage)
            return f"{self.name} атакует и наносит {self.damage} урона!"
        return f"{self.name} повержен!"