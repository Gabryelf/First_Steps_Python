import pygame
import consts
import sprites
from CollidableObject import CollidableObject
from RenderableObject import RenderableObject
import random


class Asteroid(RenderableObject,CollidableObject):
    def __init__(self,speed):
        self.is_good = random.randint(1,100) <= 30
        self.image = sprites.asteroid_image if not  self.is_good else sprites.asteroid_good_image
        self.x = consts.screen_width
        self.y = random.randint(60,consts.screen_height-self.height)
        self.height = 60 + random.randint(-5,5)
        self.width = 63 + random.randint(-5,5)
        self.image = pygame.transform.scale(self.image, (self.height,self.width))
        self.rect = self.image.get_rect(center = self.rect.center)
        self.rect.x = consts.screen_width
        self.rect.y = self.y
        self.speed = speed + random.randint(-100,100)/10

    def move(self):
        self.rect.x -= self.speed

    def draw(self,surface):
        surface.blit(self.image,self.rect)
