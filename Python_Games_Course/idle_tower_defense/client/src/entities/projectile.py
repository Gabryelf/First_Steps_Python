from dataclasses import dataclass
from typing import Tuple, Optional, TYPE_CHECKING
import math
from client.src.utils.logger import logger

if TYPE_CHECKING:
    from .enemy import Enemy

@dataclass
class Projectile:
    """Класс снаряда для стрельбы башни - ТОЛЬКО логика"""

    def __init__(self, start_pos: Tuple[float, float], target: 'Enemy', damage: float, speed: float = 5.0):
        self.position = start_pos
        self.target = target
        self.damage = damage
        self.speed = speed
        self.active = True
        self.radius = 5
        self.color = (255, 255, 0)

        logger.debug(f"Projectile created targeting {target.type.name}")

    def update(self) -> bool:
        """Обновление позиции снаряда. Возвращает True если достиг цели"""
        if not self.active:
            return True

        if not self.target.is_alive():
            self.active = False
            return True

        # Движение к цели
        target_pos = self.target.center_position
        dx = target_pos[0] - self.position[0]
        dy = target_pos[1] - self.position[1]
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < self.speed + self.target.radius:
            # Снаряд достиг цели - наносим урон
            self.target.take_damage(self.damage)
            self.active = False
            return True

        # Нормализация направления
        if distance > 0:
            dx /= distance
            dy /= distance

        # Перемещение
        self.position = (
            self.position[0] + dx * self.speed,
            self.position[1] + dy * self.speed
        )

        return False