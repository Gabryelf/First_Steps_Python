from CollidableObject import CollidableObject
from WolfAndEggConsts import WolfAndEggConsts as consts
class Player(CollidableObject):
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = consts.screen_width / 2 - self.width / 2
        self.y = consts.screen_height - self.height
        self.player_speed = 5

    def move_left(self):
        if self.collide_with_left_border():
            self.x -= self.player_speed

    def move_right(self):
        if self.collide_with_right_border():
            self.x += self.player_speed

