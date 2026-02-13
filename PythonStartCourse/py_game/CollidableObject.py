from WolfAndEggConsts import WolfAndEggConsts as consts


class CollidableObject():
    x = 0
    y = 0
    heigth = 0
    width = 0

    def collide(self,collide_object):
        return collide_object.y + collide_object.height > self.y and collide_object.x + collide_object.width > self.x and collide_object.x < self.x + collide_object.width

    def get_parametres(self):
        return (self.x, self.y, self.width, self.height)

    def collide_with_right_border(self):
        return self.x < consts.screen_width - self.width

    def collide_with_left_border(self):
        return self.x > 0

    def collide_with_bottom_border(self):
        return self.y > consts.screen_height
