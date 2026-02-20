import pygame
import color
import consts


class RenderEngine:
    def __init__(self):
        self.surface = pygame.display.set_mode(consts.screen_params)
        self.render_queue = []

    def render(self):
        self.surface.fill(color.green)
        for render_object in self.render_queue:
            render_object.draw(self.surface)
        pygame.display.update()
        self.render_queue.clear()

    def add_render_object(self, *renders_object):
        for render_object in renders_object:
            self.render_queue.append(render_object)
