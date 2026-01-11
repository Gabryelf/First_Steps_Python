from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle


class Ground(Widget):
    speed = NumericProperty(300)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (1200, 50)
        self.pos = (0, 150)

        with self.canvas:
            # Основная земля
            Color(0.3, 0.3, 0.3, 1)
            Rectangle(pos=self.pos, size=self.size)

            # Линии на земле
            Color(0.4, 0.4, 0.4, 1)
            for i in range(24):
                x = self.x + i * 50
                Rectangle(pos=(x, self.y), size=(2, 20))

    def update(self, dt):
        self.x -= self.speed * dt
        if self.x <= -600:
            self.x = 0