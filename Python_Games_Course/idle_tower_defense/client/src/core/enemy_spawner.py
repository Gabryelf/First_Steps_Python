import random
import math
from typing import List, Tuple
from client.src.utils.config import config
from client.src.utils.logger import logger


class EnemySpawner:
    """Система спавна врагов по периметру экрана"""

    def __init__(self):

        self.spawn_margin = 50  # Отступ от краев экрана для спавна
        logger.info("EnemySpawner initialized")

    def get_random_spawn_position(self) -> Tuple[float, float]:
        """Получение случайной позиции спавна на периметре экрана"""
        # Выбираем случайную сторону экрана: 0=верх, 1=право, 2=низ, 3=лево
        side = random.randint(0, 3)

        if side == 0:  # Верх
            x = random.randint(self.spawn_margin, config.SCREEN_WIDTH - self.spawn_margin)
            y = -self.spawn_margin
        elif side == 1:  # Право
            x = config.SCREEN_WIDTH + self.spawn_margin
            y = random.randint(self.spawn_margin, config.SCREEN_HEIGHT - self.spawn_margin)
        elif side == 2:  # Низ
            x = random.randint(self.spawn_margin, config.SCREEN_WIDTH - self.spawn_margin)
            y = config.SCREEN_HEIGHT + self.spawn_margin
        else:  # Лево
            x = -self.spawn_margin
            y = random.randint(self.spawn_margin, config.SCREEN_HEIGHT - self.spawn_margin)

        return (x, y)

    def get_spawn_positions_for_wave(self, wave_number: int, enemy_count: int) -> List[Tuple[float, float]]:
        """Получение позиций спавна для волны"""
        positions = []

        for _ in range(enemy_count):
            positions.append(self.get_random_spawn_position())

        return positions