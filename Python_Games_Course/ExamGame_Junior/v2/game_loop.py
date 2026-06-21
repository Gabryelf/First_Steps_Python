import pygame
from config import *
from player import Player
from objects import ObjectManager
from sounds import SoundManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ловец")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.reset_game()
        self.sound_manager = SoundManager()

    def reset_game(self):
        self.player = Player()
        self.object_manager = ObjectManager()
        self.score = 0
        self.lives = INITIAL_LIVES
        self.frame_count = 0
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # Движение игрока
        keys = pygame.key.get_pressed()
        self.player.move(keys)

        # Создание и движение объектов
        self.object_manager.create_object(self.frame_count)
        self.object_manager.move_objects()

        # Проверка столкновений
        score_change, lives_change = self.object_manager.check_collisions(self.player.get_rect())
        self.score += score_change
        self.lives += lives_change

        if score_change > 0:
            self.sound_manager.play_catch()
        if lives_change < 0:
            self.sound_manager.play_miss()

        # Проверка конца игры
        if self.lives <= 0:
            self.running = False

        self.frame_count += 1

    def draw(self):
        self.screen.fill(WHITE)

        # Отрисовка объектов
        self.object_manager.draw_objects(self.screen)

        # Отрисовка игрока
        self.player.draw(self.screen)

        # Отрисовка UI
        score_text = self.font.render(f"Счет: {self.score}", True, BLUE)
        lives_text = self.font.render(f"Жизни: {self.lives}", True, RED)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()