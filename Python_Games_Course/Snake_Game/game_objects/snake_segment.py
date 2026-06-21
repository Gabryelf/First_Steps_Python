import pygame
from core.game_object import GameObject


class SnakeSegment(GameObject):
    def __init__(self, x: int, y: int, size: int = 20):
        self.x = x
        self.y = y
        self.size = size

    def update(self):
        # Сегменты змейки обновляются через голову
        pass

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (0, 255, 0),
                         (self.x, self.y, self.size, self.size))
        # Добавляем границы для лучшей видимости
        pygame.draw.rect(surface, (0, 200, 0),
                         (self.x, self.y, self.size, self.size), 1)

    def get_position(self) -> tuple[int, int]:
        return self.x, self.y

    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y
