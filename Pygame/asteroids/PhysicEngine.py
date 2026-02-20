import pygame.mask


class PhysicEngine:
    @staticmethod
    def collide_with_left_border(collidable_object):
        return collidable_object.rect.x < 0-collidable_object.width

    @staticmethod
    def collide(collidable_object,collidable_object1):
        offset = (collidable_object1.rect.x - collidable_object.rect.x,collidable_object1.rect.y-collidable_object.rect.y)
        mask1 = pygame.mask.from_surface(collidable_object.image)
        mask2 = pygame.mask.from_surface(collidable_object1.image)
        return mask2.overlap(mask1,offset)
