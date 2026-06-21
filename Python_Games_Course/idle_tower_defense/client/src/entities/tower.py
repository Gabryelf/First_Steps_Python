from dataclasses import dataclass
from typing import List, Optional, Tuple
import math
import time
import random
from client.src.utils.config import config
from client.src.utils.logger import logger


@dataclass
class TowerStats:
    """Характеристики башни"""
    damage: float = 1.0
    attack_speed: float = 1.0  # Атак в секунду
    attack_range: float = 200.0
    critical_chance: float = 0.1  # 10%
    critical_multiplier: float = 2.0
    max_health: float = 100.0

    @property
    def attack_cooldown(self) -> float:
        """Время между атаками (в секундах)"""
        return 1.0 / self.attack_speed if self.attack_speed > 0 else float('inf')


class Tower:
    """Класс башни игрока - ТОЛЬКО логика, без рендеринга"""

    def __init__(self):
        self.position = config.screen_center
        self.base_stats = TowerStats()
        self.current_stats = TowerStats()
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100

        # Здоровье башни
        self.health = self.current_stats.max_health
        self.max_health = self.current_stats.max_health

        # Система стрельбы
        self.projectiles: List['Projectile'] = []
        self.last_attack_time = 0
        self.current_target: Optional['Enemy'] = None

        # Визуальные параметры (только данные, не логика отрисовки)
        self.radius = 50
        self.color = (70, 130, 180)  # Steel blue

        logger.info("Tower created")

    def take_damage(self, damage: float) -> bool:
        """Получение урона башней. Возвращает True если башня уничтожена"""
        self.health -= damage
        logger.debug(f"Tower took {damage} damage. Health: {self.health}/{self.max_health}")

        if self.health <= 0:
            logger.info("Tower destroyed!")
            return True
        return False

    def heal(self, amount: float) -> None:
        """Восстановление здоровья башни"""
        self.health = min(self.max_health, self.health + amount)
        logger.debug(f"Tower healed {amount}. Health: {self.health}/{self.max_health}")

    def is_alive(self) -> bool:
        """Проверка, жива ли башня"""
        return self.health > 0

    @property
    def health_ratio(self) -> float:
        """Отношение текущего здоровья к максимальному"""
        return self.health / self.max_health

    def update(self, delta_time: float, enemies: List['Enemy']) -> List['Projectile']:
        """Обновление логики башни. Возвращает новые снаряды"""
        new_projectiles = []

        # Если башня уничтожена, не стреляем
        if not self.is_alive():
            return new_projectiles

        # Поиск цели
        if not self.current_target or not self.current_target.is_alive():
            self.current_target = self._find_target(enemies)

        # Стрельба по цели
        current_time = time.time()
        if (self.current_target and
                current_time - self.last_attack_time >= self.current_stats.attack_cooldown):

            if self._is_target_in_range(self.current_target):
                projectile = self._shoot_at_target(self.current_target)
                new_projectiles.append(projectile)
                self.last_attack_time = current_time
            else:
                # Цель вышла из радиуса - ищем новую
                self.current_target = None

        # Обновление существующих снарядов
        self._update_projectiles()

        return new_projectiles

    def _find_target(self, enemies: List['Enemy']) -> Optional['Enemy']:
        """Поиск цели в радиусе атаки - всегда ближайший враг"""
        # Фильтруем только живых врагов в радиусе атаки
        valid_targets = [
            enemy for enemy in enemies
            if enemy.is_alive() and self._is_target_in_range(enemy)
        ]

        if not valid_targets:
            return None

        # Всегда выбираем ближайшего врага
        return min(valid_targets, key=lambda e: self._distance_to(e))

    def _is_target_in_range(self, enemy: 'Enemy') -> bool:
        """Проверка, находится ли враг в радиусе атаки"""
        return self._distance_to(enemy) <= self.current_stats.attack_range

    def _distance_to(self, enemy: 'Enemy') -> float:
        """Расстояние до врага"""
        dx = enemy.center_position[0] - self.position[0]
        dy = enemy.center_position[1] - self.position[1]
        return math.sqrt(dx * dx + dy * dy)

    def _shoot_at_target(self, target: 'Enemy') -> 'Projectile':
        """Создание снаряда для атаки цели"""
        damage = self.current_stats.damage

        # Критический удар
        if random.random() < self.current_stats.critical_chance:
            damage *= self.current_stats.critical_multiplier
            logger.debug("Critical hit!")

        from .projectile import Projectile
        projectile = Projectile(self.position, target, damage)
        logger.debug(f"Tower shooting at {target.type.name} for {damage} damage")
        return projectile

    def _update_projectiles(self):
        """Обновление состояния снарядов"""
        self.projectiles = [p for p in self.projectiles if p.active]

    def add_projectile(self, projectile: 'Projectile'):
        """Добавление снаряда для отслеживания"""
        self.projectiles.append(projectile)

    def add_experience(self, amount: int):
        """Добавить опыт башне"""
        self.experience += amount
        logger.debug(f"Tower gained {amount} XP. Total: {self.experience}/{self.experience_to_next_level}")

        # Проверка уровня
        while self.experience >= self.experience_to_next_level:
            self.level_up()

    def level_up(self):
        """Повышение уровня башни"""
        self.level += 1
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)

        # Автоматическое улучшение характеристик при уровне
        self.current_stats.damage *= 1.1
        self.current_stats.attack_speed *= 1.05
        self.current_stats.max_health *= 1.2
        self.max_health = self.current_stats.max_health

        # Полное восстановление здоровья при уровне
        self.health = self.max_health

        logger.info(f"Tower reached level {self.level}! Health: {self.health}")

    def can_level_up(self) -> bool:
        """Можно ли повысить уровень"""
        return self.experience >= self.experience_to_next_level