# Размеры экрана
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Размер ячейки
CELL_SIZE = 30
TANK_SIZE = 1  # танк занимает 1x1 ячейку

# Размеры поля в ячейках
FIELD_WIDTH = SCREEN_WIDTH // CELL_SIZE
FIELD_HEIGHT = (SCREEN_HEIGHT - 80) // CELL_SIZE  # Увеличили панель до 80 пикселей

# Цвета (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (205, 133, 63)
ORANGE = (255, 165, 0)

# Настройки игры
PLAYER_LIVES = 3
ENEMY_LIVES = 1
MAX_ENEMIES = 3
WALL_HITS_TO_BREAK = 3
SPAWN_POINTS = 5

# Скорости
PLAYER_SPEED = 0.25  # Ещё немного уменьшил для точности
ENEMY_SPEED = 0.2    # Боты чуть медленнее игрока
BULLET_SPEED = 1.0

# Задержки
PLAYER_SHOOT_DELAY = 45
ENEMY_SHOOT_DELAY = 90  # Увеличили задержку стрельбы ботов

# Настройки коллизий (уменьшенный хитбокс танка)
TANK_HITBOX_REDUCE = 0.7  # хитбокс будет 70% от размера ячейки

# Настройки текста
FONT_SIZE_SMALL = 24
FONT_SIZE_MEDIUM = 36
FONT_SIZE_LARGE = 48