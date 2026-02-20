import pygame
import sprites
from CollidableObject import CollidableObject
from RenderableObject import RenderableObject


class Player(CollidableObject,RenderableObject):
    def __init__(self,x,y):
        self.image = sprites.player_image
        self.lives = 3
        self.is_dead = False
        self.speed = 5
        self.x = x
        self.y = y
        self.height = 30
        self.width = 60
        self.image = pygame.transform.scale(self.image, (self.height, self.width))
        self.rect = self.image.get_rect(center = self.rect.center)
        self.rect.x = x
        self.rect.y = y

    def move(self,directoin):
        if directoin == "-x":
            self.rect.x -= self.speed
        if directoin == "x":
            self.rect.x += self.speed
        if directoin == "y":
            self.rect.y += self.speed
        if directoin == "-y":
            self.rect.y -= self.speed

    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def damaged(self):
        self.lives -= 1
        self.is_dead = self.lives <= 0
