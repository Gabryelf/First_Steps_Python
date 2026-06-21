import pygame
import random

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ловец")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Переменные игрока
player_width = 100
player_height = 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 30
player_speed = 10

# Список для падающих объектов
objects = []
effects = []

object_speed = 5
object_spawn_rate = 25  # Чем меньше, тем чаще
score = 0
font = pygame.font.SysFont(None, 36)

# Главный игровой цикл
running = True
frame_count = 0
while running:
    frame_count += 1
    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Движение игрока
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Создание нового объекта
    if frame_count % object_spawn_rate == 0:
        obj_type = "good" if random.random() > 0.2 else "bad"  # 80% хороших, 20% плохих
        obj_x = random.randint(0, WIDTH - 30)
        objects.append({"rect": pygame.Rect(obj_x, 0, 30, 30), "type": obj_type})

    # Движение и отрисовка объектов
    for obj in objects[:]:
        obj["rect"].y += object_speed
        color = GREEN if obj["type"] == "good" else RED
        pygame.draw.rect(screen, color, obj["rect"])

        # Проверка столкновения с игроком
        if obj["rect"].colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
            if obj["type"] == "good":
                score += 1
            else:
                score -= 1
                effects.append({"pos": [obj["rect"].x, obj["rect"].y], "timer": 10})
            objects.remove(obj)
        # Удаление объекта, если он упал за экран
        elif obj["rect"].y > HEIGHT:
            objects.remove(obj)

    # Отрисовка игрока и счета
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
    score_text = font.render(f"Счет: {score}", True, BLUE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
