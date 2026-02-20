import pygame
import SoundController
import color
import consts
from Fruit import Fruit
from RenderEngine import RenderEngine
from Snake import Snake


class SnakeGame:

    def __init__(self):
        pygame.init()
        SoundController.main_music.play(-1)
        self.render = RenderEngine()
        self.clock = pygame.time.Clock()
        self.font_style = pygame.font.SysFont(None, 35)
        self.game_over = False
        self.game_close = False
        self.snake = Snake(color.black,10)
        self.fruit = None

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.snake.move(-self.snake.speed, 0)
                elif event.key == pygame.K_RIGHT:
                    self.snake.move(self.snake.speed, 0)
                elif event.key == pygame.K_UP:
                    self.snake.move(0, -self.snake.speed)
                elif event.key == pygame.K_DOWN:
                    self.snake.move(0, self.snake.speed)

    def game_logic(self):
        if self.fruit is None:
            self.fruit = Fruit()
        self.event_handler()
        if self.snake.collide(self.fruit):
            self.snake.eat()
            self.fruit.destroy()
            self.fruit = Fruit()
        self.snake.update()
        if self.snake.collide_with_screen_border():
            self.game_over = True

        self.clock.tick(consts.game_FPS)

    def game_loop(self):
        while not self.game_over:
            self.game_logic()
            self.render.add_render_object(self.fruit,self.snake)
            self.render.render()
        pygame.quit()
        quit()
        