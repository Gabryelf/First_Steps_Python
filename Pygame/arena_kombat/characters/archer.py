# characters/archer.py - класс лучника

import random

import pygame
from arena_kombat.characters.base_hero import BaseHero
from arena_kombat.skills.skills_data import ARCHER_SKILLS
from arena_kombat.config.settings import DEFAULT_STATS


class Archer(BaseHero):
    """Класс лучника - высокий шанс крита и уворота"""

    def __init__(self, x, y, is_player=True):
        stats = DEFAULT_STATS['archer'].copy()
        skills = ARCHER_SKILLS.copy()

        super().__init__(
            x=x,
            y=y,
            name='Лучник',
            stats=stats,
            skills=skills,
            sprite_path=None,  # пока без спрайта
            is_player=is_player
        )

        # Специфичные для лучника параметры
        self.color = (100, 200, 100) if is_player else (150, 100, 100)
        self.create_placeholder_sprite()

        # Дополнительные характеристики лучника
        self.precision_stacks = 0  # стаки точности
        self.evasion_bonus = 0  # бонус к увороту

    def use_skill(self, skill_key, target):
        """Переопределённый метод использования навыков для лучника"""
        result = super().use_skill(skill_key, target)

        if result and result.get('success'):
            if skill_key == 'q':
                # Точный выстрел увеличивает стаки точности
                self.precision_stacks += 1
                if self.precision_stacks >= 3:
                    # Каждый 3-й точный выстрел гарантирует крит
                    self.stats['crit_chance'] = 1.0
                    result['message'] = 'Точность достигла максимума! Следующий удар гарантированно критический!'
                else:
                    result['message'] = f'Точный выстрел! Точность: {self.precision_stacks}/3'

            elif skill_key == 'w':
                # Уклонение даёт временный бонус к увороту
                self.evasion_bonus = 30
                result['message'] = 'Уклонение активировано! Шанс уворота увеличен на 30%'

            elif skill_key == 'e':
                # Град стрел - множественные удары
                result = self.multi_shot(target)

        return result

    def multi_shot(self, target):
        """Специальная атака: град стрел (3 удара)"""
        total_damage = 0
        hit_count = 0
        messages = []

        for i in range(3):
            # Каждый удар с отдельным расчётом
            base_damage = self.stats['attack'] * 0.8  # 80% от обычного урона

            # Шанс крита для каждого удара
            is_crit = random.random() < self.stats['crit_chance']
            if is_crit:
                base_damage *= 1.5

            # Шанс уворота цели
            is_dodge = random.random() < target.stats['dodge_chance']
            if not is_dodge:
                damage_reduction = target.stats['defense'] / (target.stats['defense'] + 100)
                final_damage = int(base_damage * (1 - damage_reduction))
                final_damage = max(1, final_damage)
                total_damage += final_damage
                hit_count += 1
                messages.append(f"Стрела {i + 1}: {final_damage} урона")

        target.stats['hp'] -= total_damage

        message = f'Град стрел! Попаданий: {hit_count}, общий урон: {total_damage}'

        return {
            'success': True,
            'damage': total_damage,
            'hit_count': hit_count,
            'message': message
        }

    def update(self):
        """Обновление состояния лучника"""
        super().update()

        # Обновление бонусов
        if self.evasion_bonus > 0:
            self.evasion_bonus -= 1

        # Сброс стаков точности после использования ульты
        if self.precision_stacks >= 3:
            self.precision_stacks = 0
            self.stats['crit_chance'] = DEFAULT_STATS['archer']['crit_chance']

    def get_dodge_chance(self):
        """Получить шанс уворота с учётом бонусов"""
        base_dodge = self.stats['dodge_chance']
        bonus = self.evasion_bonus / 100
        return min(0.75, base_dodge + bonus)  # максимум 75% уворота

    def draw(self, screen):
        """Отрисовка лучника с дополнительными эффектами"""
        super().draw(screen)

        # Отрисовка индикатора точности
        if self.precision_stacks > 0:
            font = pygame.font.Font(None, 20)
            precision_text = font.render(f"Точность: {self.precision_stacks}/3", True, (255, 255, 100))
            text_x = self.x - precision_text.get_width() // 2
            text_y = self.y - self.height - 25
            screen.blit(precision_text, (text_x, text_y))

        # Отрисовка эффекта уклонения
        if self.evasion_bonus > 0:
            # Рисуем эффект ветра вокруг лучника
            wind_surf = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
            for i in range(3):
                offset = random.randint(-5, 5)
                pygame.draw.line(wind_surf, (200, 200, 255, 150),
                                 (self.width // 2 + offset, 0),
                                 (self.width // 2 + offset, self.height),
                                 2)
            screen.blit(wind_surf, (self.x - self.width // 2 - 5, self.y - self.height // 2 - 5))