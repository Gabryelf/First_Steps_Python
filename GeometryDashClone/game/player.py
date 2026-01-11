from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty, ListProperty
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Rotate


class Player(Widget):
    velocity_y = NumericProperty(0)
    is_jumping = BooleanProperty(False)
    gravity = NumericProperty(-1800)
    jump_force = NumericProperty(520)
    rotation = NumericProperty(0)
    size = ListProperty([40, 40])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos = (100, 200)
        self.ground_level = 200
        self.target_rotation = 0

        with self.canvas:
            PushMatrix()
            self.rotate_inst = Rotate(angle=self.rotation, origin=self.center)
            Color(1, 0.2, 0.2, 1)  # Красный куб
            self.rect = Rectangle(pos=self.pos, size=self.size)
            PopMatrix()

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = self.jump_force
            self.is_jumping = True
            self.target_rotation = 360

    def update(self, dt):
        # Гравитация
        self.velocity_y += self.gravity * dt
        self.y += self.velocity_y * dt

        # Вращение
        if self.is_jumping:
            if self.rotation < self.target_rotation:
                self.rotation += 15
            else:
                self.rotation = self.target_rotation

        # Земля
        if self.y <= self.ground_level:
            self.y = self.ground_level
            self.velocity_y = 0
            self.is_jumping = False
            self.rotation = 0
            self.target_rotation = 0

        # Обновляем графику
        self.rect.pos = self.pos
        self.rotate_inst.origin = self.center
        self.rotate_inst.angle = self.rotation