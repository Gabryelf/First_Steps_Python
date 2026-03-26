# characters/base_hero.py - базовый класс героя

import pygame
from arena_kombat.config.settings import *


class BaseHero:
    """Базовый класс для всех героев"""

    def __init__(self, x, y, name, stats, skills, sprite_path, is_player=True):
        self.name = name
        self.x = x
        self.y = y
        self.is_player = is_player
        self.is_facing_right = is_player  # Игрок смотрит вправо, враг влево

        # Характеристики
        self.stats = stats.copy()
        self.stats['hp'] = self.stats['max_hp']
        self.stats['energy'] = self.stats['max_energy']

        # Навыки
        self.skills = skills

        # Состояния
        self.state = 'idle'  # idle, walk, jump, attack, hit, block
        self.current_action = 'idle'
        self.action_timer = 0
        self.is_grounded = True
        self.vel_y = 0

        # Анимация
        self.sprite_sheet = None
        self.current_frame = 0
        self.frame_timer = 0

        # Размеры
        self.width = 50
        self.height = 60

        # Загрузка спрайта (заглушка)
        self.color = GREEN if is_player else RED
        self.create_placeholder_sprite()

    def create_placeholder_sprite(self):
        """Создать временный спрайт (пока нет графики)"""
        self.placeholder_surf = pygame.Surface((self.width, self.height))
        self.placeholder_surf.fill(self.color)
        pygame.draw.rect(self.placeholder_surf, WHITE, self.placeholder_surf.get_rect(), 2)

    def move_left(self):
        """Движение влево"""
        if self.x > LEFT_BOUND:
            self.x -= self.stats['speed']
            self.is_facing_right = False
            if self.is_grounded and self.state != 'attack':
                self.set_state('walk')

    def move_right(self):
        """Движение вправо"""
        if self.x < RIGHT_BOUND:
            self.x += self.stats['speed']
            self.is_facing_right = True
            if self.is_grounded and self.state != 'attack':
                self.set_state('walk')

    def jump(self):
        """Прыжок"""
        if self.is_grounded and self.state != 'attack':
            self.vel_y = -12
            self.is_grounded = False
            self.set_state('jump')

    def update_physics(self):
        """Обновление физики"""
        self.vel_y += 0.8  # гравитация
        self.y += self.vel_y

        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.is_grounded = True
            self.vel_y = 0
            if self.state == 'jump' and self.action_timer <= 0:
                self.set_state('idle')

    def update_energy(self):
        """Обновление энергии"""
        if self.state != 'attack' and self.state != 'block':
            self.stats['energy'] = min(
                self.stats['energy'] + self.stats['energy_regen'],
                self.stats['max_energy']
            )

    def set_state(self, state):
        """Установка состояния"""
        if state != self.state:
            self.state = state
            self.action_timer = 0

    def take_damage(self, damage, is_crit=False):
        """Получение урона"""
        self.stats['hp'] -= damage
        self.set_state('hit')
        self.action_timer = 20  # анимация получения урона 20 кадров
        return self.stats['hp'] <= 0

    def use_skill(self, skill_key, target):
        """Использование навыка"""
        skill = self.skills.get(skill_key)
        if not skill:
            return None

        result = skill.use(self, target)
        if result and result.get('success'):
            self.set_state('attack')
            self.action_timer = 30  # анимация атаки

        return result

    def update(self):
        """Обновление состояния героя"""
        # Обновление таймера действия
        if self.action_timer > 0:
            self.action_timer -= 1
            if self.action_timer == 0 and self.state in ['attack', 'hit']:
                self.set_state('idle')

        # Обновление физики
        self.update_physics()

        # Обновление энергии
        self.update_energy()

    def draw(self, screen):
        """Отрисовка героя"""
        # Временная отрисовка прямоугольником
        surf = self.placeholder_surf
        if not self.is_facing_right:
            surf = pygame.transform.flip(surf, True, False)

        screen.blit(surf, (self.x - self.width // 2, self.y - self.height))

        # Отрисовка полоски HP
        hp_percent = self.stats['hp'] / self.stats['max_hp']
        hp_width = 100
        hp_height = 8
        hp_x = self.x - hp_width // 2
        hp_y = self.y - self.height - 10

        pygame.draw.rect(screen, RED, (hp_x, hp_y, hp_width, hp_height))
        pygame.draw.rect(screen, GREEN, (hp_x, hp_y, hp_width * hp_percent, hp_height))

        # Отрисовка полоски энергии
        energy_percent = self.stats['energy'] / self.stats['max_energy']
        energy_width = 100
        energy_height = 4
        energy_x = self.x - energy_width // 2
        energy_y = hp_y - 8

        pygame.draw.rect(screen, GRAY, (energy_x, energy_y, energy_width, energy_height))
        pygame.draw.rect(screen, BLUE, (energy_x, energy_y, energy_width * energy_percent, energy_height))

        # Имя героя
        font = pygame.font.Font(None, 20)
        name_text = font.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(self.x, hp_y - 12))
        screen.blit(name_text, name_rect)