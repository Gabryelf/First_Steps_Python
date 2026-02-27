# game.py
import pygame
import random
from config import *
from game_objects import GameObject, Player, Enemy, Bullet


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("TANKS")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.running = True
        self.game_over = False

        self.player = Player(FIELD_WIDTH // 2, FIELD_HEIGHT // 2)
        self.enemies = []
        self.walls = []
        self.bullets = []
        self.create_level()

    def create_level(self):
        for x in range(0, FIELD_WIDTH, 3):
            self.walls.append(GameObject(x, 0, 1, BROWN))
            self.walls.append(GameObject(x, FIELD_HEIGHT - 1, 1, BROWN))
        for y in range(0, FIELD_HEIGHT, 3):
            self.walls.append(GameObject(0, y, 1, BROWN))
            self.walls.append(GameObject(FIELD_WIDTH - 1, y, 1, BROWN))

        for _ in range(20):
            x, y = random.randint(5, FIELD_WIDTH - 6), random.randint(5, FIELD_HEIGHT - 6)
            self.walls.append(GameObject(x, y, 1, BROWN))

    def spawn_enemy(self):
        if len(self.enemies) >= MAX_ENEMIES:
            return
        x, y = random.randint(5, FIELD_WIDTH - 6), random.randint(5, FIELD_HEIGHT - 6)
        for obj in self.walls + self.enemies + [self.player]:
            if abs(obj.x - x) < 2 and abs(obj.y - y) < 2:
                return
        self.enemies.append(Enemy(x, y))

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        dx, dy = self.player.handle_input(keys)
        if dx != 0 or dy != 0:
            self.player.move(dx, dy, self.walls, self.enemies)
        self.player.update()

        for enemy in self.enemies:
            enemy.update()
            enemy.update_ai(self.walls, self.enemies, self.player)
            if enemy.cooldown == 0 and random.random() < 0.01:
                bullet = enemy.shoot()
                if bullet:
                    self.bullets.append(bullet)

        for bullet in self.bullets[:]:
            if bullet.dir == 0:
                bullet.y -= BULLET_SPEED
            elif bullet.dir == 1:
                bullet.x += BULLET_SPEED
            elif bullet.dir == 2:
                bullet.y += BULLET_SPEED
            else:
                bullet.x -= BULLET_SPEED

            if bullet.x < 0 or bullet.x > FIELD_WIDTH or bullet.y < 0 or bullet.y > FIELD_HEIGHT:
                self.bullets.remove(bullet)
                continue

            bullet_rect = bullet.rect()
            for wall in self.walls:
                if bullet_rect.colliderect(wall.rect()):
                    self.bullets.remove(bullet)
                    break

            if bullet.owner != self.player and bullet_rect.colliderect(self.player.rect()):
                self.game_over = True
                self.bullets.remove(bullet)

            for enemy in self.enemies[:]:
                if bullet.owner != enemy and bullet_rect.colliderect(enemy.rect()):
                    self.enemies.remove(enemy)
                    self.player.score += 1
                    self.bullets.remove(bullet)
                    break

        if random.random() < 0.01:
            self.spawn_enemy()

    def draw(self):
        self.screen.fill(BLACK)

        if not self.game_over:
            for wall in self.walls:
                pygame.draw.rect(self.screen, wall.color, wall.rect())
            for enemy in self.enemies:
                pygame.draw.rect(self.screen, enemy.color, enemy.rect())
            pygame.draw.rect(self.screen, self.player.color, self.player.rect())
            for bullet in self.bullets:
                pygame.draw.rect(self.screen, bullet.color, bullet.rect())

        pygame.draw.rect(self.screen, GRAY, (0, 0, SCREEN_WIDTH, 60))
        score_text = self.font.render(f"STAR {self.player.score}", True, YELLOW)
        self.screen.blit(score_text, (20, 10))

        if self.game_over:
            over_text = self.font.render("GAME OVER", True, RED)
            over_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(over_text, over_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_over:
                        bullet = self.player.shoot()
                        if bullet:
                            self.bullets.append(bullet)
                    elif event.key == pygame.K_r and self.game_over:
                        self.__init__()

            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
