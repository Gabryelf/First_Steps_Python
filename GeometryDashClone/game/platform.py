from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty
from kivy.graphics import Color, Rectangle


class Platform(Widget):
    speed = NumericProperty(300)  # Скорость в пикселях в секунду
    has_spike = BooleanProperty(False)

    def __init__(self, x_pos, width=200, has_spike=False, **kwargs):
        super().__init__(**kwargs)
        self.has_spike = has_spike
        self.size = (width, 20)
        self.pos = (x_pos, 150)

        with self.canvas:
            # Основная платформа
            Color(0.2, 0.6, 1.0, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

            # Декоративные линии на платформе
            Color(0.1, 0.3, 0.8, 1)
            line_spacing = 20
            for i in range(int(width / line_spacing)):
                x = self.x + i * line_spacing
                Rectangle(pos=(x, self.y), size=(2, self.height))

            if has_spike:
                Color(1, 0, 0, 1)
                spike_size = 20
                # Рисуем шип в конце платформы
                from kivy.graphics import Triangle
                points = [
                    self.right, self.top,
                    self.right - spike_size, self.top,
                    self.right - spike_size / 2, self.top + spike_size
                ]
                Triangle(points=points)

    def update(self, dt):
        self.x -= self.speed * dt

    def is_off_screen(self):
        return self.x < -self.width

    def is_player_on_platform(self, player):
        # Игрок стоит на платформе если:
        # - Его нижняя часть близко к верху платформы
        # - Он движется вниз или стоит
        # - Он находится над платформой по X
        return (player.right > self.x + 10 and
                player.x < self.right - 10 and
                player.y >= self.top - 5 and
                player.y <= self.top + 10 and
                player.velocity_y <= 0)

    def collides_with_spike(self, player):
        if not self.has_spike:
            return False
        # Столкновение с шипом в конце платформы
        spike_x = self.right - 20
        return (player.right > spike_x and
                player.x < self.right and
                player.top > self.top)