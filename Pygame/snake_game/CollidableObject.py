import pygame
import consts


class CollidableObject:
    x = 0
    y = 0
    height = 0
    width = 0
    rect = pygame.Rect(x, y, width, height)

    def collide(self, collide_object):
        return collide_object.rect.colliderect(self.rect)

    def collide_with_right_border(self):
        return self.rect.x > consts.screen_width - self.width

    def collide_with_left_border(self):
        return self.rect.x < 0

    def collide_with_bottom_border(self):
        return self.rect.y > consts.screen_height

    def collide_with_top_border(self):
        return self.rect.y < 0

    def collide_with_screen_border(self):
        return self.collide_with_right_border() \
            or self.collide_with_left_border() \
            or self.collide_with_bottom_border() \
            or self.collide_with_top_border()
