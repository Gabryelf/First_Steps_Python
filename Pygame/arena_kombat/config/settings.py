# settings.py - глобальные настройки игры

import pygame

# Размеры экрана
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Цвета (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

# Границы арены
GROUND_Y = 450
LEFT_BOUND = 100
RIGHT_BOUND = SCREEN_WIDTH - 100

# Параметры героев
DEFAULT_STATS = {
    'warrior': {
        'max_hp': 120,
        'attack': 20,
        'defense': 15,
        'speed': 5,
        'max_energy': 100,
        'energy_regen': 2,
        'crit_chance': 0.15,
        'dodge_chance': 0.05
    },
    'mage': {
        'max_hp': 80,
        'attack': 30,
        'defense': 5,
        'speed': 4,
        'max_energy': 150,
        'energy_regen': 4,
        'crit_chance': 0.20,
        'dodge_chance': 0.10
    },
    'archer': {
        'max_hp': 90,
        'attack': 25,
        'defense': 8,
        'speed': 6,
        'max_energy': 120,
        'energy_regen': 3,
        'crit_chance': 0.25,
        'dodge_chance': 0.15
    }
}