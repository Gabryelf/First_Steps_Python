from .tile import Tile

"""Класс реализации пустого участка суши с проходимостью и реализацией рендеринга"""


class GrassTile(Tile):
    """Grass - plane to run for units"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    @property
    def is_passable(self) -> bool:
        return True

    def __str__(self) -> str:
        return "G"
