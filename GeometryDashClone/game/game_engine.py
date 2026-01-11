from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
import random

from .player import Player
from .obstacle import Obstacle
from .ground import Ground
from .background import Background
from .particle import Particle


class GameEngine(Widget):
    score = NumericProperty(0)
    is_game_running = BooleanProperty(False)
    game_speed = NumericProperty(300)
    game_state = StringProperty("menu")  # menu, playing, game_over

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player()
        self.ground = Ground()
        self.background = Background()
        self.obstacles = []
        self.particles = []

        self.obstacle_timer = 0
        self.obstacle_interval = 1.5
        self.last_obstacle_x = 800

        self.setup_graphics()
        Window.bind(on_key_down=self.on_key_down)

    def setup_graphics(self):
        # Добавляем игровые объекты
        self.add_widget(self.background)
        self.add_widget(self.ground)
        self.add_widget(self.player)

        # Счетчик очков
        with self.canvas:
            Color(1, 1, 1, 1)
            self.score_label = Rectangle(pos=(650, 550), size=(140, 40))

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 32:  # SPACE
            if self.game_state == "menu":
                self.start_game()
            elif self.game_state == "playing":
                self.player.jump()
            elif self.game_state == "game_over":
                self.restart_game()

    def start_game(self):
        self.game_state = "playing"
        self.is_game_running = True
        self.score = 0
        self.game_speed = 300
        self.obstacles = []
        self.particles = []
        self.obstacle_timer = 0
        self.last_obstacle_x = 800

        # Очищаем препятствия
        for obstacle in self.obstacles[:]:
            self.remove_widget(obstacle)
        self.obstacles.clear()

        # Запускаем игровой цикл
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.update, 1 / 60.)

    def restart_game(self):
        self.start_game()

    def game_over(self):
        self.game_state = "game_over"
        self.is_game_running = False
        Clock.unschedule(self.update)

    def create_particles(self, x, y):
        for _ in range(8):
            particle = Particle(x, y)
            self.particles.append(particle)
            self.add_widget(particle)

    def update(self, dt):
        if not self.is_game_running:
            return

        # Обновляем объекты
        self.player.update(dt)
        self.ground.speed = self.game_speed
        self.ground.update(dt)

        # Генерация препятствий
        self.obstacle_timer += dt
        if self.obstacle_timer >= self.obstacle_interval:
            self.generate_obstacle()
            self.obstacle_timer = 0

        # Обновляем препятствия
        for obstacle in self.obstacles[:]:
            obstacle.speed = self.game_speed
            obstacle.update(dt)

            # Проверка столкновений
            if obstacle.collides_with_player(self.player):
                self.create_particles(self.player.center_x, self.player.center_y)
                self.game_over()
                return

            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                self.remove_widget(obstacle)
                self.score += 1

        # Обновляем частицы
        for particle in self.particles[:]:
            particle.update(dt)
            if particle.is_dead():
                self.particles.remove(particle)
                self.remove_widget(particle)

        # Увеличиваем сложность
        self.game_speed += dt * 5
        self.obstacle_interval = max(0.8, 1.5 - self.score * 0.01)

    def generate_obstacle(self):
        obstacle_type = random.randint(0, 2)
        min_distance = 300 + random.randint(0, 200)

        new_x = max(self.width, self.last_obstacle_x + min_distance)
        obstacle = Obstacle(new_x, obstacle_type)

        self.obstacles.append(obstacle)
        self.add_widget(obstacle)
        self.last_obstacle_x = new_x

    def on_touch_down(self, touch):
        if self.game_state == "menu":
            self.start_game()
        elif self.game_state == "playing":
            self.player.jump()
        elif self.game_state == "game_over":
            self.restart_game()
        return True

    def draw_ui(self):
        # Отрисовка UI
        with self.canvas:
            Color(1, 1, 1, 1)
            Line(rectangle=(650, 550, 140, 40), width=2)

            if self.game_state == "menu":
                Color(1, 1, 1, 1)
                Rectangle(pos=(300, 300), size=(200, 60))
            elif self.game_state == "game_over":
                Color(1, 0, 0, 1)
                Rectangle(pos=(300, 300), size=(200, 60))