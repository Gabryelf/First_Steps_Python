from abc import ABC, abstractmethod
from typing import Tuple, Any

from client.src.utils.config import config
from client.src.utils.logger import logger


class Renderer(ABC):
    """Абстрактный базовый класс для системы рендеринга"""

    def __init__(self):
        self.screen = None
        self.logger = logger

    @abstractmethod
    def initialize(self) -> bool:
        """Инициализация рендерера"""
        pass

    @abstractmethod
    def clear_screen(self):
        """Очистка экрана"""
        pass

    @abstractmethod
    def draw_rectangle(self, rect: Tuple[float, float, float, float], color: Tuple[int, int, int]):
        """Отрисовка прямоугольника"""
        pass

    @abstractmethod
    def draw_circle(self, center: Tuple[float, float], radius: float, color: Tuple[int, int, int]):
        """Отрисовка круга"""
        pass

    @abstractmethod
    def draw_text(self, text: str, position: Tuple[float, float], color: Tuple[int, int, int], size: int = 24):
        """Отрисовка текста"""
        pass

    @abstractmethod
    def update_display(self):
        """Обновление дисплея"""
        pass


class PygameRenderer(Renderer):
    """Реализация рендерера на Pygame"""

    def initialize(self) -> bool:
        """Инициализация Pygame и создание окна"""
        try:
            import pygame
            self.pygame = pygame

            pygame.init()
            self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            pygame.display.set_caption(config.GAME_TITLE)

            self.font = pygame.font.Font(None, 36)  # Стандартный шрифт

            self.logger.info("Pygame renderer initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize Pygame renderer: {e}")
            return False

    def clear_screen(self):
        """Очистка экрана цветом фона"""
        self.screen.fill(config.BACKGROUND_COLOR)

    def draw_rectangle(self, rect: Tuple[float, float, float, float], color: Tuple[int, int, int]):
        """Отрисовка прямоугольника"""
        self.pygame.draw.rect(self.screen, color, rect)

    def draw_circle(self, center: Tuple[float, float], radius: float, color: Tuple[int, int, int], width: int = 0):
        """Отрисовка круга
        Args:
            center: Центр круга (x, y)
            radius: Радиус круга
            color: Цвет в формате RGB
            width: Толщина линии (0 - заливка, >0 - контур)
        """
        self.pygame.draw.circle(self.screen, color, (int(center[0]), int(center[1])), int(radius), width)

    def draw_text(self, text: str, position: Tuple[float, float], color: Tuple[int, int, int], size: int = 24):
        """Отрисовка текста"""
        font = self.pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def update_display(self):
        """Обновление дисплея"""
        self.pygame.display.flip()