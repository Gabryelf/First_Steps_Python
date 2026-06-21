from abc import ABC, abstractmethod

""" Абстракция для всех тайлов в игре, каждый тайл должен знать свои координаты,
контракт проходимости и рендеринга для более конкретных тайлов объектов"""
class Tile(ABC):
    """Basic abstract class from all tiles in game"""

    # инициализация тайла
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # проходимость тайла
    @property
    @abstractmethod
    def is_passable(self) -> bool:
        pass

    # рендеринг для консоли - требуется заменить на более подходящий в будущем
    def __str__(self) -> str:
        pass




