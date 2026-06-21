import pygame
import time
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
objects = []
effects = []

object_speed = 5
object_spawn_rate = 25

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


while True:
    time.sleep(0.1)
    obj_type = "good" if random.random() > 0.2 else "bad"  # 80% хороших, 20% плохих
    obj_x = random.randint(0, WIDTH - 30)
    objects.append({"rect": pygame.Rect(obj_x, 0, 30, 30), "type": obj_type})

    for obj in objects[:]:
        obj["rect"].y += object_speed
        color = GREEN if obj["type"] == "good" else RED
        if obj["type"] != "good":
            pygame.draw.rect(screen, color, obj["rect"])

        if obj["rect"].colliderect(pygame.Rect(300, 300, 300, 300)):
            if obj["type"] == "bad":
                effects.append({"pos": [obj["rect"].x, obj["rect"].y], "timer": 10})
                time.sleep(0.2)
            objects.remove(obj)
        # Удаление объекта, если он упал за экран
        elif obj["rect"].y > HEIGHT:
            objects.remove(obj)

        pygame.display.flip()
        for effect in effects[:]:
            pygame.draw.circle(screen, RED, effect["pos"], 50)
            effect["timer"] -= 1
            if effect["timer"] <= 0:
                effects.remove(effect)

