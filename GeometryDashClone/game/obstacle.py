from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle, Triangle, Line
import math


class Obstacle(Widget):
    speed = NumericProperty(300)

    def __init__(self, x_pos, obstacle_type=0, **kwargs):
        super().__init__(**kwargs)
        self.type = obstacle_type

        if obstacle_type == 0:  # Шип
            self.size = (50, 50)
            self.pos = (x_pos, 200)
            with self.canvas:
                Color(1, 0, 0, 1)
                points = [self.center_x, self.top, self.x, self.y, self.right, self.y]
                Triangle(points=points)

        elif obstacle_type == 1:  # Пила
            self.size = (60, 60)
            self.pos = (x_pos, 200)
            with self.canvas:
                Color(0.5, 0.5, 0.5, 1)
                Line(circle=(self.center_x, self.center_y, 25), width=2)
                # Зубья пилы
                for i in range(8):
                    angle = math.radians(i * 45)
                    x1 = self.center_x + 20 * math.cos(angle)
                    y1 = self.center_y + 20 * math.sin(angle)
                    x2 = self.center_x + 30 * math.cos(angle)
                    y2 = self.center_y + 30 * math.sin(angle)
                    Line(points=[x1, y1, x2, y2], width=2)

        elif obstacle_type == 2:  # Блок
            self.size = (50, 50)
            self.pos = (x_pos, 200)
            with self.canvas:
                Color(0.2, 0.6, 1, 1)
                Rectangle(pos=self.pos, size=self.size)
                Color(0.1, 0.3, 0.8, 1)
                Line(rectangle=(self.x, self.y, self.width, self.height), width=2)

    def update(self, dt):
        self.x -= self.speed * dt

    def is_off_screen(self):
        return self.x < -100

    def collides_with_player(self, player):
        if self.type == 0:  # Шип
            return (player.collide_point(self.center_x, self.y + 25) or
                    player.collide_point(self.x + 10, self.y + 10) or
                    player.collide_point(self.right - 10, self.y + 10))

        elif self.type == 1:  # Пила
            distance = math.sqrt((player.center_x - self.center_x) ** 2 +
                                 (player.center_y - self.center_y) ** 2)
            return distance < 35

        elif self.type == 2:  # Блок
            return (player.right > self.x and player.x < self.right and
                    player.top > self.y and player.y < self.top)