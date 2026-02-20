import pygame
import sprites
import consts


class RenderEngine:
    def __init__(self):
        self.screen = pygame.display.set_mode(consts.screen_params)
        pygame.display.set_caption(consts.game_title)
        self.background_rect = sprites.background_image.get_rect()
        self.render_queue_list = []
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
    def render_frame(self,lives,score):
        self.screen.blit(sprites.background_image, self.background_rect)
        self.__render_queue()
        lives_text = self.font.render(f"Lives: {lives}", True, (0, 0, 0))
        self.screen.blit(lives_text, (10, 10))

        # Отображение счетчика очков
        score_text = self.font.render(f"Score: {score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 50))
        pygame.display.update()

    def __render_queue(self):
        for render_object in self.render_queue_list:
            render_object.draw(self.screen)
        self.render_queue_list.clear()

    def add_render_object(self, *renders_object):
        for render_object in renders_object:
            self.render_queue_list.append(render_object)
