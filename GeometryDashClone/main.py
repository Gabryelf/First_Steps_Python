from kivy.app import App
from kivy.core.window import Window


class GeometryDashApp(App):
    def build(self):
        Window.size = (800, 600)
        from game.game_engine import GameEngine
        return GameEngine()


if __name__ == '__main__':
    GeometryDashApp().run()