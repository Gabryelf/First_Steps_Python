"""
Tiles package - все типы тайлов должны быть импортированы здесь для удобного доступа
"""

from .tile import Tile
from .grass import GrassTile
from .mountain import MountainTile

__all__ = ['Tile', 'GrassTile', 'MountainTile']