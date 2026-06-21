from typing import List, Dict, Any, Callable, Optional, Tuple
import pygame
from client.src.ui.components import UIComponent, Button
from client.src.utils.config import config
from client.src.utils.logger import logger


class UpgradePanel(UIComponent):
    """Панель улучшений башни"""

    def __init__(self, rect: Tuple[float, float, float, float]):
        super().__init__(rect)
        self.upgrade_buttons: List[Button] = []
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.upgrade_system = None
        self.tower = None
        self.game_state = None

        # Цвета
        self.bg_color = (50, 50, 70)
        self.header_color = (80, 80, 120)
        self.button_color = (70, 130, 180)
        self.button_hover_color = (100, 160, 200)
        self.disabled_color = (100, 100, 100)

    def set_systems(self, upgrade_system, tower, game_state):
        """Установка ссылок на системы"""
        self.upgrade_system = upgrade_system
        self.tower = tower
        self.game_state = game_state
        self._create_upgrade_buttons()

    def _create_upgrade_buttons(self):
        """Создание кнопок улучшений"""
        if not self.upgrade_system:
            return

        self.upgrade_buttons.clear()
        upgrades_info = self.upgrade_system.get_all_upgrades_info()

        button_height = 80
        button_width = self.rect.width - 20
        y_offset = 60  # Отступ для заголовка

        for upgrade_name, info in upgrades_info.items():
            button_rect = (self.rect.x + 10, self.rect.y + y_offset, button_width, button_height)

            # Создаем функцию обратного вызова для этой кнопки
            def create_callback(upgrade_name=upgrade_name):
                return lambda: self._on_upgrade_click(upgrade_name)

            button = Button(button_rect, "", create_callback())
            button.color = self.button_color
            button.hover_color = self.button_hover_color
            self.upgrade_buttons.append(button)

            y_offset += button_height + 10

    def _on_upgrade_click(self, upgrade_name: str):
        """Обработчик клика по улучшению"""
        if not self.upgrade_system or not self.tower or not self.game_state:
            return

        success, message = self.upgrade_system.apply_upgrade(upgrade_name, self.tower, self.game_state)
        if success:
            logger.info(f"Upgrade successful: {message}")
            # Можно добавить визуальную обратную связь
        else:
            logger.warning(f"Upgrade failed: {message}")

    def draw(self, screen):
        """Отрисовка панели улучшений"""
        if not self.visible or not self.upgrade_system:
            return

        # Фон панели
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (100, 100, 120), self.rect, 2, border_radius=8)

        # Заголовок
        title_text = "Улучшения башни"
        title_surface = self.font.render(title_text, True, (255, 255, 255))
        screen.blit(title_surface, (self.rect.x + 10, self.rect.y + 10))

        # Информация о монетах
        if self.game_state:
            coins_text = f"Монеты: {self.game_state.player_progress.coins}"
            coins_surface = self.small_font.render(coins_text, True, (255, 255, 0))
            screen.blit(coins_surface, (self.rect.x + 10, self.rect.y + 35))

        # Кнопки улучшений
        upgrades_info = self.upgrade_system.get_all_upgrades_info()

        for i, (upgrade_name, button) in enumerate(zip(upgrades_info.keys(), self.upgrade_buttons)):
            info = upgrades_info[upgrade_name]

            # Обновляем состояние кнопки
            can_upgrade, _ = self.upgrade_system.can_upgrade(upgrade_name,
                                                             self.game_state.player_progress.coins if self.game_state else 0)
            button.color = self.button_color if can_upgrade else self.disabled_color

            # Отрисовка кнопки
            button.draw(screen)

            # Текст улучшения
            self._draw_upgrade_info(screen, button.rect, info, can_upgrade)

    def _draw_upgrade_info(self, screen, button_rect, info: Dict[str, Any], can_upgrade: bool):
        """Отрисовка информации об улучшении на кнопке"""
        text_color = (255, 255, 255) if can_upgrade else (150, 150, 150)

        # Название и уровень
        name_text = f"{info['name']} (Ур. {info['current_level']}/{info['max_level']})"
        name_surface = self.small_font.render(name_text, True, text_color)
        screen.blit(name_surface, (button_rect.x + 10, button_rect.y + 5))

        # Описание
        desc_surface = self.small_font.render(info['description'], True, text_color)
        screen.blit(desc_surface, (button_rect.x + 10, button_rect.y + 25))

        # Стоимость
        cost_text = f"Стоимость: {info['next_cost']} монет"
        cost_surface = self.small_font.render(cost_text, True, (255, 255, 0))
        screen.blit(cost_surface, (button_rect.x + 10, button_rect.y + 55))

    def handle_event(self, event) -> bool:
        """Обработка событий"""
        if not self.visible:
            return False

        for button in self.upgrade_buttons:
            if button.handle_event(event):
                return True

        return False