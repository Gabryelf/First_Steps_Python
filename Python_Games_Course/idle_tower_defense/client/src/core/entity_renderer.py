import pygame
import random
from typing import List, Tuple

from ..entities.tower import Tower
from ..entities.enemy import Enemy
from ..entities.projectile import Projectile
from ..utils.logger import logger


class EntityRenderer:
    """Рендерер для игровых сущностей - ТОЛЬКО отрисовка, без логики"""

    def __init__(self) -> None:
        self.logger = logger
        self.hit_effects: List[dict] = []  # Эффекты попадания

    def add_hit_effect(self, position: Tuple[float, float], damage: float):
        """Добавление эффекта попадания"""
        self.hit_effects.append({
            'position': position,
            'damage': damage,
            'timer': 1.0,  # 1 секунда
            'color': (255, 100, 100)  # Красный цвет для урона
        })

    def draw_hit_effects(self, screen: pygame.Surface):
        """Отрисовка эффектов попадания"""
        for effect in self.hit_effects[:]:
            # Уменьшаем таймер
            effect['timer'] -= 0.016  # ~60 FPS

            if effect['timer'] <= 0:
                self.hit_effects.remove(effect)
                continue

            # Рисуем текст урона
            font = pygame.font.Font(None, 20)
            damage_text = f"-{effect['damage']}"
            text_surface = font.render(damage_text, True, effect['color'])

            # Добавляем дрожание для эффекта
            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)

            text_rect = text_surface.get_rect(center=(
                int(effect['position'][0]) + offset_x,
                int(effect['position'][1]) - 20 + offset_y
            ))

            screen.blit(text_surface, text_rect)

    def draw_tower(self, screen: pygame.Surface, tower: Tower) -> None:
        """Отрисовка башни с полоской здоровья"""
        # Тело башни
        pygame.draw.circle(screen, tower.color,
                           (int(tower.position[0]), int(tower.position[1])),
                           tower.radius)

        # Полоска здоровья башни
        if tower.max_health > 0:
            health_width = 80
            health_height = 8
            health_x = tower.position[0] - health_width // 2
            health_y = tower.position[1] - tower.radius - 15

            # Фон полоски здоровья
            pygame.draw.rect(screen, (255, 0, 0),
                             (health_x, health_y, health_width, health_height))

            # Текущее здоровье
            current_health_width = max(2, health_width * tower.health_ratio)
            health_color = (0, 255, 0) if tower.health_ratio > 0.3 else (255, 165, 0)
            pygame.draw.rect(screen, health_color,
                             (health_x, health_y, current_health_width, health_height))

    def draw_enemy(self, screen: pygame.Surface, enemy: Enemy) -> None:
        """Отрисовка врага с полоской здоровья"""
        if not enemy.is_alive():
            return

        # Тело врага
        pygame.draw.circle(screen, enemy.color,
                           (int(enemy.position[0]), int(enemy.position[1])),
                           enemy.radius)

        # Полоска здоровья
        health_width = 40
        health_height = 6
        health_x = enemy.position[0] - health_width // 2
        health_y = enemy.position[1] - enemy.radius - 10

        # Фон полоски здоровья
        pygame.draw.rect(screen, (255, 0, 0),
                         (health_x, health_y, health_width, health_height))

        # Текущее здоровье
        current_health_width = max(2, health_width * enemy.health_ratio)
        health_color = (0, 255, 0) if enemy.health_ratio > 0.3 else (255, 165, 0)
        pygame.draw.rect(screen, health_color,
                         (health_x, health_y, current_health_width, health_height))

    def draw_projectile(self, screen: pygame.Surface, projectile: Projectile) -> None:
        """Отрисовка снаряда"""
        if projectile.active:
            # Рисуем снаряд с небольшим свечением
            pygame.draw.circle(screen, projectile.color,
                               (int(projectile.position[0]), int(projectile.position[1])),
                               projectile.radius)

            # Эффект свечения
            glow_color = (255, 255, 100)  # Более яркий желтый
            pygame.draw.circle(screen, glow_color,
                               (int(projectile.position[0]), int(projectile.position[1])),
                               projectile.radius - 1)

    def draw_battle_entities(self, screen: pygame.Surface, tower: Tower,
                             enemies: List[Enemy], projectiles: List[Projectile]) -> None:
        """Отрисовка всех боевых сущностей"""
        # Башня (рисуется первой, чтобы быть под другими элементами)
        self.draw_tower(screen, tower)

        # Враги
        for enemy in enemies:
            self.draw_enemy(screen, enemy)

        # Снаряды (рисуются последними, чтобы быть поверх других элементов)
        for projectile in projectiles:
            self.draw_projectile(screen, projectile)

        # Эффекты попадания (самые верхние)
        self.draw_hit_effects(screen)