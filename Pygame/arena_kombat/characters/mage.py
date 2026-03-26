# characters/mage.py - класс мага
import pygame
from arena_kombat.characters.base_hero import BaseHero
from arena_kombat.skills.skills_data import MAGE_SKILLS
from arena_kombat.config.settings import DEFAULT_STATS


class Mage(BaseHero):
    """Класс мага - высокий урон, низкая защита"""

    def __init__(self, x, y, is_player=True):
        stats = DEFAULT_STATS['mage'].copy()
        skills = MAGE_SKILLS.copy()

        super().__init__(
            x=x,
            y=y,
            name='Маг',
            stats=stats,
            skills=skills,
            sprite_path=None,  # пока без спрайта
            is_player=is_player
        )

        # Специфичные для мага параметры
        self.color = (100, 100, 250) if is_player else (200, 100, 250)
        self.create_placeholder_sprite()

        # Дополнительные характеристики мага
        self.mana_shield = False  # магический щит
        self.shield_timer = 0

    def use_skill(self, skill_key, target):
        """Переопределённый метод использования навыков для мага"""
        result = super().use_skill(skill_key, target)

        # Дополнительная логика для мага
        if skill_key == 'w' and result and result.get('success'):
            # Активация магического щита
            self.mana_shield = True
            self.shield_timer = 180  # 3 секунды (60 FPS)
            result['message'] = 'Магический щит активирован!'

        return result

    def update(self):
        """Обновление состояния мага"""
        super().update()

        # Обновление магического щита
        if self.mana_shield:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.mana_shield = False

    def take_damage(self, damage, is_crit=False):
        """Получение урона с учётом магического щита"""
        if self.mana_shield:
            # Щит поглощает 50% урона
            damage = int(damage * 0.5)
            self.add_log_effect("Магический щит поглотил часть урона!")

        return super().take_damage(damage, is_crit)

    def add_log_effect(self, message):
        """Добавление эффекта в лог (заглушка)"""
        # В реальной игре здесь была бы отправка в систему логов
        pass

    def draw(self, screen):
        """Отрисовка мага с дополнительными эффектами"""
        super().draw(screen)

        # Отрисовка эффекта магического щита
        if self.mana_shield:
            # Рисуем полупрозрачный круг вокруг мага
            shield_surf = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
            pygame.draw.circle(shield_surf, (100, 100, 255, 100),
                               (self.width // 2 + 10, self.height // 2 + 10),
                               self.width // 2 + 5)
            screen.blit(shield_surf, (self.x - self.width // 2 - 10, self.y - self.height // 2 - 10))