# main.py - точка входа в игру

import pygame
import sys
from config.settings import *
from game.game_state import GameState


class Game:
    """Главный класс игры"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Battle Arena")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameState(self.screen)

    def run(self):
        """Главный игровой цикл"""
        while self.running:
            dt = self.clock.tick(60)  # 60 FPS

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.game_state.handle_event(event)

            # Обновление
            self.game_state.update(dt)

            # Отрисовка
            self.game_state.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
