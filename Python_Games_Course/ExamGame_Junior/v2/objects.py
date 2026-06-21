# objects.py
import pygame
import random
from config import *


class ObjectManager:
    def __init__(self):
        self.objects = []
        self.speed = OBJECT_SPEED
        self.spawn_rate = OBJECT_SPAWN_RATE

    def create_object(self, frame_count):
        if frame_count % self.spawn_rate == 0:
            obj_type = "good" if random.random() < GOOD_OBJECT_CHANCE else "bad"
            obj_x = random.randint(0, WIDTH - OBJECT_SIZE)
            new_object = {
                "rect": pygame.Rect(obj_x, 0, OBJECT_SIZE, OBJECT_SIZE),
                "type": obj_type
            }
            self.objects.append(new_object)

    def move_objects(self):
        for obj in self.objects[:]:
            obj["rect"].y += self.speed

            # Удаляем объекты, упавшие за экран
            if obj["rect"].y > HEIGHT:
                self.objects.remove(obj)

    def draw_objects(self, screen):
        for obj in self.objects:
            color = GREEN if obj["type"] == "good" else RED
            pygame.draw.rect(screen, color, obj["rect"])

    def check_collisions(self, player_rect):
        score_change = 0
        lives_change = 0

        for obj in self.objects[:]:
            if obj["rect"].colliderect(player_rect):
                if obj["type"] == "good":
                    score_change += 1
                else:
                    lives_change -= 1
                self.objects.remove(obj)

        return score_change, lives_change
    