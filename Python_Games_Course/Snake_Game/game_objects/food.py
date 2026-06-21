from typing import List
import random
import pygame
from core.game_object import GameObject


class Food(GameObject):
    def __init__(self, x: int, y: int, size: int = 20):
        self.x = x
        self.y = y
        self.size = size

    def update(self):
        # Еда не обновляется сама по себе
        pass

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (255, 0, 0),
                         (self.x, self.y, self.size, self.size))

    def get_position(self) -> tuple[int, int]:
        return self.x, self.y

    def respawn(self, max_x: int, max_y: int, occupied_positions: List[tuple[int, int]]):
        while True:
            # Выравниваем по сетке
            self.x = random.randint(0, (max_x - self.size) // self.size) * self.size
            self.y = random.randint(0, (max_y - self.size) // self.size) * self.size

            # Проверяем, чтобы еда не появилась на занятой позиции
            food_pos = self.get_position()
            collision = food_pos in occupied_positions

            if not collision:
                break
