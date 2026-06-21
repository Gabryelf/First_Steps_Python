"""
Core package for the game engine.
Этот файл делает папку core Python-пакетом и задает публичный API
"""

# Делаем ключевые классы доступными напрямую из core
from .map import GameMap
from .game import GameController

__all__ = ['GameMap', 'GameController']