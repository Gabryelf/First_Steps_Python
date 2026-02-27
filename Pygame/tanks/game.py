import pygame
import os
import random
from config import *
from game_objects import PlayerTank, EnemyTank, Wall, Bullet


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Танчики")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

        self.player = None
        self.enemies = []
        self.walls = []
        self.bullets = []
        self.spawn_points = []

        self.score = 0
        self.high_score = self.load_high_score()
        self.start_time = pygame.time.get_ticks()
        self.game_over = False

        self.create_level()

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def create_level(self):
        """Создает уровень с лабиринтом"""
        # Очищаем списки
        self.walls = []
        self.spawn_points = []

        # Создаем стены по краям (делаем поле замкнутым)
        for x in range(FIELD_WIDTH):
            self.walls.append(Wall(x, 0))
            self.walls.append(Wall(x, FIELD_HEIGHT - 1))

        for y in range(FIELD_HEIGHT):
            if y > 0 and y < FIELD_HEIGHT - 1:  # Чтобы не дублировать углы
                self.walls.append(Wall(0, y))
                self.walls.append(Wall(FIELD_WIDTH - 1, y))

        # Создаем внутренний лабиринт
        for _ in range(80):  # Количество стен
            x = random.randint(2, FIELD_WIDTH - 3)
            y = random.randint(2, FIELD_HEIGHT - 3)

            # Проверяем, не слишком близко к краю и другим стенам
            too_close = False
            for wall in self.walls:
                if abs(wall.x - x) < 2 and abs(wall.y - y) < 2:
                    too_close = True
                    break

            if not too_close:
                # Создаем группу стен
                if random.random() < 0.6:
                    # Горизонтальная линия
                    length = random.randint(2, 4)
                    for i in range(length):
                        if x + i < FIELD_WIDTH - 1:
                            self.walls.append(Wall(x + i, y))
                else:
                    # Вертикальная линия
                    length = random.randint(2, 4)
                    for i in range(length):
                        if y + i < FIELD_HEIGHT - 1:
                            self.walls.append(Wall(x, y + i))

        # Создаем точки спавна
        for _ in range(SPAWN_POINTS):
            for attempt in range(50):  # Пробуем 50 раз найти свободное место
                x = random.randint(5, FIELD_WIDTH - 6)
                y = random.randint(5, FIELD_HEIGHT - 6)

                # Проверяем, свободно ли место
                free = True
                for wall in self.walls:
                    if abs(wall.x - x) < 3 and abs(wall.y - y) < 3:
                        free = False
                        break

                if free:
                    self.spawn_points.append((float(x), float(y)))
                    break

        # Создаем игрока в центре
        center_x = float(FIELD_WIDTH // 2)
        center_y = float(FIELD_HEIGHT // 2)
        self.player = PlayerTank(center_x, center_y)

    def spawn_enemy(self):
        """Создает нового врага"""
        if len(self.enemies) >= MAX_ENEMIES or not self.spawn_points:
            return

        # Выбираем свободную точку спавна
        random.shuffle(self.spawn_points)
        for spawn_point in self.spawn_points:
            free = True

            # Проверяем, не занято ли место другими танками
            for enemy in self.enemies:
                if abs(enemy.x - spawn_point[0]) < 2 and abs(enemy.y - spawn_point[1]) < 2:
                    free = False
                    break

            # Проверяем, не занято ли место игроком
            if self.player and abs(self.player.x - spawn_point[0]) < 2 and \
                    abs(self.player.y - spawn_point[1]) < 2:
                free = False

            if free:
                self.enemies.append(EnemyTank(spawn_point[0], spawn_point[1]))
                break

    def update_bullets(self):
        """Обновляет пули и проверяет попадания"""
        for bullet in self.bullets[:]:
            # Двигаем пулю
            if bullet.direction == 0:
                bullet.y -= bullet.speed
            elif bullet.direction == 1:
                bullet.x += bullet.speed
            elif bullet.direction == 2:
                bullet.y += bullet.speed
            else:
                bullet.x -= bullet.speed

            # Проверяем выход за границы
            if (bullet.x < 0 or bullet.x > FIELD_WIDTH or
                    bullet.y < 0 or bullet.y > FIELD_HEIGHT):
                self.bullets.remove(bullet)
                continue

            bullet_rect = bullet.get_rect()
            hit = False

            # Проверяем попадание в стены
            for wall in self.walls[:]:
                if bullet_rect.colliderect(wall.get_rect()):
                    if wall.hit():
                        self.walls.remove(wall)
                    self.bullets.remove(bullet)
                    hit = True
                    break

            if hit:
                continue

            # Проверяем попадание в игрока
            if (bullet.owner != self.player and self.player and
                    bullet_rect.colliderect(self.player.get_hitbox())):
                self.player.lives -= 1
                self.bullets.remove(bullet)
                if self.player.lives <= 0:
                    self.game_over = True
                continue

            # Проверяем попадание во врагов
            for enemy in self.enemies[:]:
                if bullet.owner != enemy and bullet_rect.colliderect(enemy.get_hitbox()):
                    enemy.lives -= 1
                    self.bullets.remove(bullet)
                    if enemy.lives <= 0:
                        self.enemies.remove(enemy)
                        self.score += 1
                        if self.score > self.high_score:
                            self.high_score = self.score
                            self.save_high_score()
                    break

    def draw_ui(self):
        """Отрисовывает красивый интерфейс"""
        # Фон панели
        panel_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 80)
        pygame.draw.rect(self.screen, DARK_GRAY, panel_rect)
        pygame.draw.line(self.screen, WHITE, (0, 80), (SCREEN_WIDTH, 80), 2)

        # Счет (звездочки) с иконкой
        star_text = self.font_large.render(f"★ {self.score}", True, YELLOW)
        self.screen.blit(star_text, (20, 15))

        # Жизни игрока с сердечками
        lives_text = self.font_large.render(f"❤ {self.player.lives}", True, RED)
        self.screen.blit(lives_text, (200, 15))

        # Таймер с иконкой часов
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = self.font_large.render(f"⏱ {minutes:02d}:{seconds:02d}", True, WHITE)
        self.screen.blit(timer_text, (400, 15))

        # Рекорд с кубком
        record_text = self.font_large.render(f"🏆 {self.high_score}", True, YELLOW)
        self.screen.blit(record_text, (650, 15))

        # Количество врагов
        enemies_text = self.font_large.render(f"💥 {len(self.enemies)}/{MAX_ENEMIES}", True, ORANGE)
        self.screen.blit(enemies_text, (900, 15))

        # Подсказки по управлению (мелким шрифтом)
        controls_text = self.font_small.render("WASD/Стрелки - движение | Пробел - стрельба", True, WHITE)
        self.screen.blit(controls_text, (SCREEN_WIDTH - 400, 50))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.player and not self.game_over:
                    if self.player.can_shoot():
                        bullet = self.player.shoot()
                        if bullet:
                            self.bullets.append(bullet)
                elif event.key == pygame.K_r and self.game_over:
                    # Перезапуск игры
                    self.__init__()

    def update(self):
        if self.game_over:
            return

        # Управление игроком
        keys = pygame.key.get_pressed()
        dx, dy = self.player.handle_input(keys)
        if dx != 0 or dy != 0:
            self.player.move(dx, dy, self.walls, self.enemies)

        self.player.update()

        # Обновление врагов
        for enemy in self.enemies:
            enemy.update()
            enemy.update_ai(self.walls, self.enemies, self.player)

            if enemy.can_shoot() and random.random() < 0.02:  # 2% шанс выстрела в кадр
                bullet = enemy.shoot()
                if bullet:
                    self.bullets.append(bullet)

        self.update_bullets()

        # Спавн новых врагов (реже)
        if random.random() < 0.005 and len(self.enemies) < MAX_ENEMIES:
            self.spawn_enemy()

    def draw(self):
        # Очищаем экран
        self.screen.fill(BLACK)

        # Рисуем сетку поля (очень бледную, для ориентира)
        if not self.game_over:
            for x in range(0, SCREEN_WIDTH, CELL_SIZE):
                pygame.draw.line(self.screen, (40, 40, 40), (x, 80), (x, SCREEN_HEIGHT), 1)
            for y in range(80, SCREEN_HEIGHT, CELL_SIZE):
                pygame.draw.line(self.screen, (40, 40, 40), (0, y), (SCREEN_WIDTH, y), 1)

        if not self.game_over:
            # Стены
            for wall in self.walls:
                wall.draw(self.screen)

            # Враги
            for enemy in self.enemies:
                enemy.draw(self.screen)

            # Игрок
            if self.player:
                self.player.draw(self.screen)

            # Пули
            for bullet in self.bullets:
                bullet.draw(self.screen)
        else:
            # Экран Game Over
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.font_large.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, text_rect)

            score_text = self.font_medium.render(f"Ваш счет: {self.score} ★", True, YELLOW)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(score_text, score_rect)

            if self.score == self.high_score and self.score > 0:
                record_text = self.font_medium.render("НОВЫЙ РЕКОРД! 🏆", True, YELLOW)
                record_rect = record_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
                self.screen.blit(record_text, record_rect)

            restart_text = self.font_small.render("Нажмите R для перезапуска", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            self.screen.blit(restart_text, restart_rect)

        # Рисуем интерфейс поверх всего
        self.draw_ui()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()