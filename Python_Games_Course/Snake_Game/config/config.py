class GameConfig:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.cell_size = 20
        self.fps = 10
        self.background_color = (0, 0, 0)
        self.score_color = (255, 255, 255)

    def get_grid_width(self) -> int:
        return self.screen_width // self.cell_size

    def get_grid_height(self) -> int:
        return self.screen_height // self.cell_size