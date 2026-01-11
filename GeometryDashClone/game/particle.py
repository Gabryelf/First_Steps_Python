from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty
from kivy.graphics import Color, Rectangle
import random


class Particle(Widget):
    life = NumericProperty(1.0)
    size = ListProperty([8, 8])

    def __init__(self, x, y, **kwargs):
        super().__init__(**kwargs)
        self.pos = (x - 4, y - 4)
        self.velocity = [random.uniform(-50, 50), random.uniform(-20, 80)]

        with self.canvas:
            Color(1, 0.5, 0.2, 0.8)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update(self, dt):
        self.life -= dt * 2
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.velocity[1] -= 200 * dt

        # Уменьшаем размер
        self.size = [max(2, 8 * self.life), max(2, 8 * self.life)]
        self.rect.size = self.size
        self.rect.pos = (self.x, self.y)

    def is_dead(self):
        return self.life <= 0