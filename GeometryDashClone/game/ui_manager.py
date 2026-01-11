from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

from .game_engine import GameEngine


class UIManager(BoxLayout):
    current_screen = StringProperty("menu")  # menu, game, game_over

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.show_menu()

    def show_menu(self):
        self.clear_widgets()
        self.current_screen = "menu"

        # Заголовок
        title = Label(
            text="GEOMETRY DASH",
            font_size='40sp',
            color=(1, 1, 1, 1),
            bold=True
        )

        # Кнопка старта
        start_btn = Button(
            text="START GAME",
            size_hint=(0.5, 0.2),
            pos_hint={'center_x': 0.5},
            background_color=(0.2, 0.7, 0.2, 1),
            font_size='20sp'
        )
        start_btn.bind(on_press=self.start_game)

        self.add_widget(title)
        self.add_widget(start_btn)

    def show_game_over(self, score):
        self.clear_widgets()
        self.current_screen = "game_over"

        # Текст Game Over
        game_over_label = Label(
            text=f"GAME OVER\nScore: {score}",
            font_size='30sp',
            color=(1, 0.2, 0.2, 1),
            bold=True
        )

        # Кнопка рестарта
        restart_btn = Button(
            text="PLAY AGAIN",
            size_hint=(0.5, 0.2),
            pos_hint={'center_x': 0.5},
            background_color=(0.2, 0.7, 0.2, 1),
            font_size='20sp'
        )
        restart_btn.bind(on_press=self.start_game)

        # Кнопка меню
        menu_btn = Button(
            text="MENU",
            size_hint=(0.5, 0.2),
            pos_hint={'center_x': 0.5},
            background_color=(0.3, 0.3, 0.8, 1),
            font_size='20sp'
        )
        menu_btn.bind(on_press=lambda x: self.show_menu())

        self.add_widget(game_over_label)
        self.add_widget(restart_btn)
        self.add_widget(menu_btn)

    def start_game(self, instance):
        self.clear_widgets()
        self.current_screen = "game"
        self.game_engine = GameEngine()
        self.game_engine.bind(on_game_over=self.on_game_over)
        self.add_widget(self.game_engine)
        self.game_engine.start_game()

    def on_game_over(self, instance, score):
        self.show_game_over(score)