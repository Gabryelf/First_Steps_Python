import pygame
import random
from config import *


class GameObject:
    def __init__(self, x, y, size, color):
        self.x = float(x)
        self.y = float(y)
        self.size = size
        self.color = color

    def rect(self):
        return pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE + 60),
                           self.size * CELL_SIZE, self.size * CELL_SIZE)


class Bullet(GameObject):
    def __init__(self, x, y, dir, owner):
        super().__init__(x, y, 0.3, YELLOW)
        self.dir = dir
        self.owner = owner


class Tank(GameObject):
    def __init__(self, x, y, color, speed):
        super().__init__(x, y, 1, color)
        self.speed = speed
        self.dir = 0
        self.cooldown = 0

    def move(self, dx, dy, walls, others):
        new_x, new_y = self.x + dx, self.y + dy
        if new_x < 0 or new_x + 1 > FIELD_WIDTH or new_y < 0 or new_y + 1 > FIELD_HEIGHT:
            return False

        new_rect = pygame.Rect(int(new_x * CELL_SIZE), int(new_y * CELL_SIZE + 60),
                               CELL_SIZE, CELL_SIZE)

        for w in walls:
            if new_rect.colliderect(w.rect()):
                return False
        for o in others:
            if o != self and new_rect.colliderect(o.rect()):
                return False

        self.x, self.y = new_x, new_y
        return True

    def shoot(self):
        if self.cooldown > 0:
            return None
        self.cooldown = 30
        return Bullet(self.x + 0.5, self.y + 0.5, self.dir, self)

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1


class Player(Tank):
    def __init__(self, x, y):
        super().__init__(x, y, GREEN, PLAYER_SPEED)
        self.score = 0

    def handle_input(self, keys):
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dir = 3
            dx = -self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dir = 1
            dx = self.speed
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.dir = 0
            dy = -self.speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.dir = 2
            dy = self.speed
        return dx, dy


class Enemy(Tank):
    def __init__(self, x, y):
        super().__init__(x, y, RED, ENEMY_SPEED)
        self.action_timer = 0
        self.action_delay = random.randint(60, 120)
        self.move_dir = random.randint(0, 3)

    def update_ai(self, walls, others, player):
        self.action_timer += 1
        if self.action_timer >= self.action_delay:
            self.action_timer = 0
            self.action_delay = random.randint(60, 120)
            if random.random() < 0.3:
                self.move_dir = random.randint(0, 3)

        dx = dy = 0
        if self.move_dir == 0:
            dy = -self.speed
        elif self.move_dir == 1:
            dx = self.speed
        elif self.move_dir == 2:
            dy = self.speed
        else:
            dx = -self.speed

        if self.move(dx, dy, walls, others + [player]):
            self.dir = self.move_dir