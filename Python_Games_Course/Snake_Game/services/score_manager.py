import pygame
from core.interfaces import Renderable


class ScoreManager(Renderable):
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.font = pygame.font.Font(None, 36)

    def increase_score(self, points: int = 10):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def draw(self, surface: pygame.Surface):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 255))

        surface.blit(score_text, (10, 10))
        surface.blit(high_score_text, (10, 50))

    def reset(self):
        self.score = 0