# config.py
import pygame

# Размеры окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Цвета (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Цвета элементов (для кружков)
COLORS = {
    "Fire": (255, 100, 0),
    "Water": (0, 100, 255),
    "Earth": (139, 69, 19),
    "Air": (200, 200, 255),
    "Steam": (192, 192, 192),
    "Mud": (101, 67, 33),
    "Lava": (255, 69, 0),
    "Cloud": (245, 245, 245),
    "Life": (34, 139, 34),
    "Dust": (180, 180, 160),
    "Stone": (128, 128, 128),
}

# Настройки интерфейса
ELEMENT_SIZE = 80
FONT_SIZE = 18