import pygame
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космический защитник")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

def create_images():
    player_img = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.polygon(player_img, BLUE, [(25, 0), (0, 50), (50, 50)])

    asteroid_img = pygame.Surface((45, 45), pygame.SRCALPHA)
    pygame.draw.circle(asteroid_img, (150, 150, 150), (22, 22), 22)

    for i in range(5):
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        pygame.draw.circle(asteroid_img, (120, 120, 120),
                           (22 + offset_x, 22 + offset_y), 8)

    bullet_img = pygame.Surface((4, 12), pygame.SRCALPHA)
    pygame.draw.rect(bullet_img, YELLOW, (0, 0, 4, 12))

    return player_img, asteroid_img, bullet_img


player_img, asteroid_img, bullet_img = create_images()

player_x = WIDTH // 2
player_y = HEIGHT - 80
player_speed = 6

asteroids = []
bullets = []
spawn_timer = 0

score = 0
lives = 3
font = pygame.font.Font(None, 36)


def create_sounds():
    shoot_sound = pygame.mixer.Sound(buffer=bytearray([]))
    explosion_sound = pygame.mixer.Sound(buffer=bytearray([]))

    return shoot_sound, explosion_sound


shoot_sound, explosion_sound = create_sounds()

def shoot_bullet():
    bullets.append({
        'x': player_x + 23,
        'y': player_y,
        'speed': 10
    })
    shoot_sound.play()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot_bullet()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > HEIGHT // 2:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - 50:
        player_y += player_speed

    # Автоматическая стрельба при зажатом пробеле
    if keys[pygame.K_SPACE] and len(bullets) < 5:
        if pygame.time.get_ticks() % 10 == 0:
            shoot_bullet()

    spawn_timer += 1
    if spawn_timer >= 40:
        asteroids.append({
            'x': random.randint(0, WIDTH - 45),
            'y': -45,
            'speed': random.randint(2, 5),
            'size': random.randint(35, 50)
        })
        spawn_timer = 0

    for bullet in bullets[:]:
        bullet['y'] -= bullet['speed']

        if bullet['y'] < -20:
            bullets.remove(bullet)

    for asteroid in asteroids[:]:
        asteroid['y'] += asteroid['speed']

        asteroid_rect = pygame.Rect(asteroid['x'], asteroid['y'], 45, 45)
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet['x'], bullet['y'], 4, 12)
            if asteroid_rect.colliderect(bullet_rect):
                explosion_sound.play()
                asteroids.remove(asteroid)
                if bullet in bullets:
                    bullets.remove(bullet)
                score += 10
                break

        player_rect = pygame.Rect(player_x, player_y, 50, 50)
        if asteroid_rect.colliderect(player_rect):
            explosion_sound.play()
            asteroids.remove(asteroid)
            lives -= 1
            if lives <= 0:
                running = False

        elif asteroid['y'] > HEIGHT:
            asteroids.remove(asteroid)

    screen.fill(BLACK)

    for asteroid in asteroids:
        screen.blit(asteroid_img, (asteroid['x'], asteroid['y']))

    for bullet in bullets:
        screen.blit(bullet_img, (bullet['x'], bullet['y']))

    screen.blit(player_img, (player_x, player_y))

    score_text = font.render(f"Счет: {score}", True, GREEN)
    lives_text = font.render(f"Жизни: {lives}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    controls_text = font.render("Стрелки: движение, Пробел: стрельба", True, WHITE)
    screen.blit(controls_text, (WIDTH // 2 - 180, HEIGHT - 30))

    pygame.display.flip()
    clock.tick(60)

game_over_text = font.render(f"Игра окончена! Счет: {score}", True, YELLOW)
screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()