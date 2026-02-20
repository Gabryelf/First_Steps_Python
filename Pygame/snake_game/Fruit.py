import pygame
import SoundController
import color
import consts
from CollidableObject import CollidableObject
from RenderObject import RenderObject
import random


class Fruit(CollidableObject, RenderObject):
    def __init__(self):
        self.color = (color.red)
        self.width = 15
        self.height = 15
        self.x = random.randint(0, consts.screen_width - self.width)
        self.y = random.randint(0, consts.screen_height - self.height)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def destroy(self):
        SoundController.fruit_eat.play()
        del self
