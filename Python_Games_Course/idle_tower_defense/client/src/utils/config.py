import os
from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class GameConfig:
    """Конфигурация игры - централизованное хранилище всех настроек"""

    # Размеры окна
    SCREEN_WIDTH: int = 1200
    SCREEN_HEIGHT: int = 700

    # Цвета (RGB)
    BACKGROUND_COLOR: Tuple[int, int, int] = (45, 45, 65)
    UI_PRIMARY_COLOR: Tuple[int, int, int] = (70, 130, 180)
    UI_SECONDARY_COLOR: Tuple[int, int, int] = (100, 160, 200)
    UI_BUTTON_COLOR: Tuple[int, int, int] = (70, 130, 180)
    UI_BUTTON_HOVER_COLOR: Tuple[int, int, int] = (100, 160, 200)
    UI_PANEL_COLOR: Tuple[int, int, int] = (60, 60, 80)

    # Настройки игры
    FPS: int = 60
    GAME_TITLE: str = "Idle Tower Defense"

    # Пути к ресурсам
    ASSETS_PATH: str = os.path.join(os.path.dirname(__file__), "../../../assets")

    @property
    def screen_center(self) -> Tuple[float, float]:
        """Центр экрана - вычисляемое свойство"""
        return (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)


# Глобальный экземпляр конфигурации
config = GameConfig()
