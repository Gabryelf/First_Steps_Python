import pygame
import random

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космический защитник")
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Игрок
player_x = WIDTH // 2
player_y = HEIGHT - 80
player_speed = 6

# Списки объектов
asteroids = []
bullets = []
spawn_timer = 0

# Игровые переменные
score = 0
lives = 3
font = pygame.font.Font(None, 36)


# Создаем простые картинки
player_img = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.polygon(player_img, BLUE, [(25, 0), (0, 50), (50, 50)])

asteroid_img = pygame.Surface((45, 45), pygame.SRCALPHA)
pygame.draw.circle(asteroid_img, (150, 150, 150), (22, 22), 22)

bullet_img = pygame.Surface((4, 12), pygame.SRCALPHA)
pygame.draw.rect(bullet_img, (255, 255, 0), (0, 0, 4, 12))

# Создаем простые звуки
shoot_sound = pygame.mixer.Sound(buffer=bytearray([]))
explosion_sound = pygame.mixer.Sound(buffer=bytearray([]))


# Функция выстрела
def shoot_bullet():
    bullets.append({
        'x': player_x + 23,
        'y': player_y,
        'speed': 10
    })
    # В функции shoot_bullet добавь:
    shoot_sound.play()


# Главный игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # В обработке событий добавь:
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot_bullet()

    # Движение игрока
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > HEIGHT // 2:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - 50:
        player_y += player_speed

    # Создание новых астероидов
    spawn_timer += 1
    if spawn_timer >= 40:
        asteroids.append({
            'x': random.randint(0, WIDTH - 45),
            'y': -45,
            'speed': random.randint(2, 5)
        })
        spawn_timer = 0

    # Движение пуль
    for bullet in bullets[:]:
        bullet['y'] -= bullet['speed']
        if bullet['y'] < -20:
            bullets.remove(bullet)

    # Движение астероидов
    for asteroid in asteroids[:]:
        asteroid['y'] += asteroid['speed']
        if asteroid['y'] > HEIGHT:
            asteroids.remove(asteroid)

    # Проверка столкновений пуль с астероидами
    for asteroid in asteroids[:]:
        asteroid_rect = pygame.Rect(asteroid['x'], asteroid['y'], 45, 45)

        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet['x'], bullet['y'], 4, 12)
            if asteroid_rect.colliderect(bullet_rect):
                asteroids.remove(asteroid)
                if bullet in bullets:
                    bullets.remove(bullet)
                    # При столкновении пули с астероидом добавь:
                    explosion_sound.play()
                score += 10
                break

        # Столкновение игрока с астероидом
        player_rect = pygame.Rect(player_x, player_y, 50, 50)
        if asteroid_rect.colliderect(player_rect):
            asteroids.remove(asteroid)
            # При столкновении игрока с астероидом добавь:
            explosion_sound.play()

            lives -= 1
            if lives <= 0:
                running = False

    # Заполняем экран черным цветом
    screen.fill(BLACK)

    # Рисуем астероиды
    for asteroid in asteroids:
        screen.blit(asteroid_img, (asteroid['x'], asteroid['y']))

    # Рисуем пули
    for bullet in bullets:
        screen.blit(bullet_img, (bullet['x'], bullet['y']))

    # Рисуем игрока
    screen.blit(player_img, (player_x, player_y))

    # Рисуем UI
    score_text = font.render(f"Счет: {score}", True, GREEN)
    lives_text = font.render(f"Жизни: {lives}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

