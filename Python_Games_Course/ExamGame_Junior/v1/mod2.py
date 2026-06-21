import pygame
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


font = pygame.font.SysFont(None, 56)
WHITE = (255, 255, 255)

lives = 3
running = True

while running:

    time.sleep(2)
    if lives <= 0:
        running = False

    lives -= 1
    lives_text = font.render(f"Жизни: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 10))

    pygame.display.flip()


