from .entity import Entity
from typing import List
import random


class Enemy(Entity):
    """Улучшенный класс врага с прогрессией"""

    def __init__(self, name: str, level: int = 1):
        # Формула сложности: базовая статистика * коэффициент уровня
        base_health = 20 + (level - 1) * 8
        base_damage = 8 + (level - 1) * 2

        super().__init__(name, base_health)
        self.level = level
        self.damage = base_damage
        self.gold_reward = 10 + level * 5
        self.exp_reward = 25 + level * 10

        # Случайное усиление для вариативности
        self._apply_random_buff()

    def _apply_random_buff(self):
        """Случайное усиление врага"""
        buffs = [
            ("strong", "Сильный", lambda: setattr(self, 'damage', int(self.damage * 1.5))),
            ("tough", "Живучий", lambda: setattr(self, '_max_health', int(self._max_health * 1.5))),
            ("fast", "Быстрый", lambda: None)  # В будущем можно добавить дополнительные ходы
        ]

        if random.random() < 0.3:  # 30% шанс на усиление
            buff_type, buff_name, apply_buff = random.choice(buffs)
            apply_buff()
            self.name = f"{buff_name} {self.name}"

    def get_available_actions(self) -> List[str]:
        return ["атаковать"]

    def make_turn(self, target: Entity) -> str:
        """Враг делает ход"""
        if self.is_alive:
            target.take_damage(self.damage)
            return f"{self.name} атакует и наносит {self.damage} урона!"
        return f"{self.name} повержен!"

    def get_rewards(self) -> dict:
        """Получить награды за победу"""
        return {
            "gold": self.gold_reward,
            "experience": self.exp_reward
        }