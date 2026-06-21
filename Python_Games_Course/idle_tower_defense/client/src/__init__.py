"""
Client package for Idle Tower Defense
"""

# Делаем все основные модули доступными напрямую
from .core.game_engine import GameEngine
from .core.game_state import GameState, GameStateType, PlayerProgress
from .core.wave_manager import WaveManager
from .core.renderer import Renderer, PygameRenderer

from .entities.tower import Tower, TowerStats
from .entities.enemy import Enemy, EnemyType

from .ui.components import UIComponent, Button, InfoPanel

from .utils.config import config
from .utils.logger import logger, GameLogger

__all__ = [
    'GameEngine', 'GameState', 'GameStateType', 'PlayerProgress', 'WaveManager',
    'Renderer', 'PygameRenderer', 'Tower', 'TowerStats', 'Enemy', 'EnemyType',
    'UIComponent', 'Button', 'InfoPanel', 'config', 'logger', 'GameLogger'
]