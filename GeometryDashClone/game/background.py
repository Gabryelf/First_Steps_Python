from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle


class Background(Widget):
    speed = NumericProperty(150)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layers = []

        # Создаем слои фона
        with self.canvas:
            # Основной фон
            Color(0.1, 0.1, 0.3, 1)
            Rectangle(pos=(0, 0), size=(800, 600))

            # Горы (задний план)
            Color(0.15, 0.15, 0.4, 1)
            for i in range(3):
                Rectangle(pos=(i * 400, 100), size=(400, 200))

            # Столбы (передний план)
            Color(0.2, 0.2, 0.5, 1)
            for i in range(8):
                Rectangle(pos=(i * 200, 150), size=(50, 100))

    def update(self, dt):
        # Простая реализация параллакса
        pass