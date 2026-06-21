import pygame
from config.config import GameConfig
from game_objects.snake import Snake
from game_objects.food import Food
from services.collision_detector import CollisionDetector
from services.score_manager import ScoreManager
from core.direction import Direction


class Game:

    def __init__(self):
        pygame.init()
        self.config = GameConfig()
        self.screen = pygame.display.set_mode(
            (self.config.screen_width, self.config.screen_height)
        )
        pygame.display.set_caption("Snake Game - OOP/SOLID Example")
        self.clock = pygame.time.Clock()

        # Инициализация компонентов (Composition)
        self.snake = Snake(
            self.config.screen_width // 2,
            self.config.screen_height // 2,
            self.config.cell_size
        )

        self.food = Food(0, 0, self.config.cell_size)
        self._respawn_food()

        self.collision_detector = CollisionDetector()
        self.score_manager = ScoreManager()
        self.running = True
        self.game_over = False

    def _respawn_food(self):
        self.food.respawn(
            self.config.screen_width,
            self.config.screen_height,
            self.snake.get_segments_positions()
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_q:
                        self.running = False
                else:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(Direction.RIGHT)

    def update(self):
        if self.game_over:
            return

        self.snake.update()

        head_position = self.snake.get_position()

        # Со стеной
        if self.collision_detector.check_wall_collision(
                head_position, self.config.screen_width, self.config.screen_height
        ):
            self.game_over = True
            return

        # С собой
        if self.snake.check_self_collision():
            self.game_over = True
            return

        # С едой
        if self.collision_detector.check_food_collision(head_position, self.food):
            self.snake.grow()
            self.score_manager.increase_score()
            self._respawn_food()

    def draw(self):
        self.screen.fill(self.config.background_color)

        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.score_manager.draw(self.screen)

        if self.game_over:
            self._draw_game_over()

        pygame.display.flip()

    def _draw_game_over(self):
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        restart_text = pygame.font.Font(None, 36).render(
            "Press R to restart or Q to quit", True, (255, 255, 255)
        )

        text_rect = game_over_text.get_rect(
            center=(self.config.screen_width // 2, self.config.screen_height // 2 - 50)
        )
        restart_rect = restart_text.get_rect(
            center=(self.config.screen_width // 2, self.config.screen_height // 2 + 50)
        )

        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(restart_text, restart_rect)

    def restart_game(self):
        self.snake = Snake(
            self.config.screen_width // 2,
            self.config.screen_height // 2,
            self.config.cell_size
        )
        self._respawn_food()
        self.score_manager.reset()
        self.game_over = False

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.config.fps)

        pygame.quit()