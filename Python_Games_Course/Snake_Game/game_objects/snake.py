from typing import List
import pygame
from core.game_object import GameObject
from core.direction import Direction
from game_objects.snake_segment import SnakeSegment


class Snake(GameObject):
    def __init__(self, x: int, y: int, size: int = 20):
        self.segments: List[SnakeSegment] = []
        self.direction = Direction.RIGHT
        self.size = size
        self.grow_pending = 3  # Начальная длина

        # Создаем начальные сегменты
        for i in range(3):
            self.segments.append(SnakeSegment(x - i * size, y, size))

    def update(self):
        head = self.segments[0]
        new_x = head.x + self.direction.value[0] * self.size
        new_y = head.y + self.direction.value[1] * self.size

        # Создаем новую голову
        new_head = SnakeSegment(new_x, new_y, self.size)

        # Добавляем новую голову в начало
        self.segments.insert(0, new_head)

        # Удаляем хвост, если не нужно расти
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.segments.pop()

    def draw(self, surface: pygame.Surface):
        for segment in self.segments:
            segment.draw(surface)

    def get_position(self) -> tuple[int, int]:
        return self.segments[0].get_position()

    def change_direction(self, new_direction: Direction):
        if new_direction != Direction.get_opposite(self.direction):
            self.direction = new_direction

    def grow(self):
        self.grow_pending += 1

    def check_self_collision(self) -> bool:
        head_pos = self.get_position()
        for segment in self.segments[1:]:
            if segment.get_position() == head_pos:
                return True
        return False

    def get_segments_positions(self) -> List[tuple[int, int]]:
        return [segment.get_position() for segment in self.segments]