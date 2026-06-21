from dataclasses import dataclass
from typing import Tuple, List
import math
from client.src.utils.config import config
from client.src.utils.logger import logger


@dataclass
class EnemyType:
    """Тип врага с характеристиками"""
    name: str
    health: float
    speed: float
    color: Tuple[int, int, int]  # Данные для рендерера
    reward: int
    experience: int


class Enemy:
    """Базовый класс врага - ТОЛЬКО логика"""

    # Предопределенные типы врагов
    TYPES = {
        "goblin": EnemyType("Goblin", 2, 0.5, (50, 180, 50), 5, 10),
        "orc": EnemyType("Orc", 4, 0.8, (180, 50, 50), 10, 20),
        "boss": EnemyType("Boss", 15, 0.4, (180, 50, 180), 30, 50)
    }

    def __init__(self, enemy_type: str, path: List[Tuple[float, float]]):
        self.type = self.TYPES[enemy_type]
        self.health = self.type.health
        self.max_health = self.type.health
        self.speed = self.type.speed
        self.color = self.type.color

        # Позиция и движение
        self.path = path
        self.current_path_index = 0
        self.position = self.path[0] if self.path else (0, 0)
        self.radius = 20
        self.reached_end = False

        # ОТЛАДКА
        logger.info(f"🎯 Enemy created: {self.type.name}")
        logger.info(f"🎯 Enemy path: {self.path}")
        logger.info(f"🎯 Enemy start position: {self.position}")
        logger.info(f"🎯 Enemy target: {self.path[-1] if self.path else 'None'}")

        logger.debug(f"Enemy {self.type.name} created")

    def take_damage(self, damage: float) -> bool:
        """Получение урона. Возвращает True если враг умер"""
        self.health -= damage
        logger.debug(f"Enemy {self.type.name} took {damage} damage. Health: {self.health}")

        if self.health <= 0:
            logger.info(f"Enemy {self.type.name} defeated!")
            return True
        return False

    def update(self, delta_time: float) -> bool:
        """Обновление позиции врага. Возвращает True если враг дошел до конца"""
        if self.reached_end:
            return True

        if self.current_path_index >= len(self.path) - 1:
            self.reached_end = True
            logger.info(f"Enemy {self.type.name} reached the tower!")
            return True

        target_pos = self.path[self.current_path_index + 1]
        dx = target_pos[0] - self.position[0]
        dy = target_pos[1] - self.position[1]
        distance = math.sqrt(dx * dx + dy * dy)

        # Если очень близко к цели, переходим к следующей точке
        if distance < 2.0:
            self.current_path_index += 1
            if self.current_path_index >= len(self.path) - 1:
                self.reached_end = True
                logger.info(f"Enemy {self.type.name} reached the tower!")
                return True
            # Рекурсивно вызываем для следующей точки
            return self.update(delta_time)

        # Движение к цели
        if distance > 0:
            direction_x = dx / distance
            direction_y = dy / distance

            # Умножаем на delta_time для плавного движения
            move_distance = self.speed * 100 * delta_time
            self.position = (
                self.position[0] + direction_x * move_distance,
                self.position[1] + direction_y * move_distance
            )

        return False

    def is_alive(self) -> bool:
        """Проверка, жив ли враг"""
        return self.health > 0

    @property
    def center_position(self) -> Tuple[float, float]:
        """Центральная позиция для отрисовки и расчетов"""
        return (self.position[0], self.position[1])

    @property
    def health_ratio(self) -> float:
        """Отношение текущего здоровья к максимальному"""
        return self.health / self.max_health