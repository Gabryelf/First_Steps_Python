import pygame
import copy
from CollidableObject import CollidableObject
from RenderObject import RenderObject


class Snake(CollidableObject,RenderObject):
    def __init__(self, color, block_size):
        self.color = color
        self.block_size = block_size
        self.snake_list = []
        self.snake_length = 1
        self.vector_x = 0
        self.vector_y = 0
        self.speed = 10
        # Начальная позиция головы змейки
        self.head = pygame.Rect(200,200,10,10)

    def move(self, x_change, y_change):
        self.vector_x = x_change
        self.vector_y = y_change

    def update(self):
        self.head.x += self.vector_x
        self.head.y += self.vector_y
        self.rect = self.head
        self.snake_list.append(copy.copy(self.head))
        if len(self.snake_list) > self.snake_length:
            del self.snake_list[0]

    def draw(self, surface):
        for part in self.snake_list:
            pygame.draw.rect(surface, self.color, part)

    def eat(self):
        self.snake_length += 1
