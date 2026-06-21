import pygame
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космический избегатель")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def create_simple_images():
    player_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.polygon(player_surf, (0, 100, 255), [(25, 0), (0, 50), (50, 50)])

    rock_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(rock_surf, (150, 150, 150), (20, 20), 20)

    return player_surf, rock_surf


player_img, rock_img = create_simple_images()

player_x = WIDTH // 2
player_y = HEIGHT - 100
player_speed = 5

rocks = []
rock_speed = 3
spawn_timer = 0

score = 0
font = pygame.font.Font(None, 36)

explosion_sound = pygame.mixer.Sound("../audio/miss.wav")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - 50:
        player_y += player_speed

    spawn_timer += 1
    if spawn_timer >= 30:
        rocks.append({
            'x': random.randint(0, WIDTH - 40),
            'y': -40,
            'speed': random.randint(3, 6)
        })
        spawn_timer = 0

    for rock in rocks[:]:
        rock['y'] += rock['speed']

        player_rect = pygame.Rect(player_x, player_y, 50, 50)
        rock_rect = pygame.Rect(rock['x'], rock['y'], 40, 40)

        if player_rect.colliderect(rock_rect):
            explosion_sound.play()
            rocks.remove(rock)
            score = max(0, score - 1)

        elif rock['y'] > HEIGHT:
            rocks.remove(rock)
            score += 1

    screen.fill(BLACK)

    for rock in rocks:
        screen.blit(rock_img, (rock['x'], rock['y']))

    screen.blit(player_img, (player_x, player_y))

    score_text = font.render(f"Счет: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
