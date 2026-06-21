from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .entity import Entity


class Card(ABC):
    """Абстрактный класс карты"""

    def __init__(self, name: str, description: str, energy_cost: int):
        self.name = name
        self.description = description
        self.energy_cost = energy_cost

    @abstractmethod
    def play(self, caster: 'Entity', target: 'Entity' = None) -> str:
        """Использование карты - абстрактный метод"""
        pass

    def __str__(self):
        return f"{self.name} ({self.energy_cost} энергии): {self.description}"