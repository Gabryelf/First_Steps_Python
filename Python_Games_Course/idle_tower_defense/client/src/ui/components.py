from typing import Tuple, Optional, Callable
import pygame
from client.src.utils.config import config
from client.src.utils.logger import logger


class UIComponent:
    """Базовый класс UI компонента"""

    def __init__(self, rect: Tuple[float, float, float, float]):
        self.rect = pygame.Rect(rect)
        self.visible = True

    def draw(self, screen):
        """Отрисовка компонента"""
        pass

    def handle_event(self, event) -> bool:
        """Обработка событий"""
        return False


class Button(UIComponent):
    """Кнопка UI"""

    def __init__(self, rect: Tuple[float, float, float, float], text: str,
                 on_click: Optional[Callable] = None):
        super().__init__(rect)
        self.text = text
        self.on_click = on_click
        self.color = config.UI_PRIMARY_COLOR
        self.hover_color = (100, 160, 200)
        self.is_hovered = False

        # Создаем шрифт
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen):
        if not self.visible:
            return

        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=5)

        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event) -> bool:
        if not self.visible:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.on_click:
                self.on_click()
                logger.debug(f"Button clicked: {self.text}")
                return True

        return False


class InfoPanel(UIComponent):
    """Панель информации"""

    def __init__(self, rect: Tuple[float, float, float, float]):
        super().__init__(rect)
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)

    def draw(self, screen, game_state):
        if not self.visible:
            return

        # Фон панели
        pygame.draw.rect(screen, (60, 60, 80), self.rect, border_radius=5)
        pygame.draw.rect(screen, (100, 100, 120), self.rect, 2, border_radius=5)

        # Текст информации
        y_offset = 10
        texts = [
            f"Coins: {game_state.player_progress.coins}",
            f"Diamonds: {game_state.player_progress.diamonds}",
            f"Wave: {game_state.player_progress.current_wave}",
            f"Score: {game_state.player_progress.score}",
            f"Enemies Defeated: {game_state.player_progress.enemies_defeated}"
        ]

        for text in texts:
            text_surface = self.small_font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (self.rect.x + 10, self.rect.y + y_offset))
            y_offset += 25