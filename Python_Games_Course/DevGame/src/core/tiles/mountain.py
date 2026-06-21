from .tile import Tile

"""Класс с реализацией гор как участков с препятствиями, тайлы которые не имеют проходимости и 
реализованы в рендеринге"""


class MountainTile(Tile):
    """Moutain - tile do not run for units"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    @property
    def is_passable(self) -> bool:
        return False

    def __str__(self) -> str:
        return "M"