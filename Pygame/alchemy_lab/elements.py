# elements.py
import pygame
from config import COLORS, ELEMENT_SIZE, FONT_SIZE, BLACK


class Element:
    """Базовый класс для всех элементов (Абстракция)"""

    def __init__(self, name, color_key, rarity=1):
        self.name = name
        self.color = COLORS.get(color_key, (150, 150, 150))
        self.rarity = rarity
        self.rect = None  # Прямоугольник для отрисовки (устанавливается в UI)
        self.font = pygame.font.Font(None, FONT_SIZE)

    def combine(self, other):
        """Полиморфный метод: возвращает новый элемент или None"""
        # Базовый класс не знает комбинаций
        return None

    def draw(self, surface, x, y):
        """Отрисовка элемента в виде кружка с текстом"""
        self.rect = pygame.Rect(x, y, ELEMENT_SIZE, ELEMENT_SIZE)
        pygame.draw.circle(surface, self.color, (x + ELEMENT_SIZE // 2, y + ELEMENT_SIZE // 2), ELEMENT_SIZE // 2)
        pygame.draw.circle(surface, (0, 0, 0), (x + ELEMENT_SIZE // 2, y + ELEMENT_SIZE // 2), ELEMENT_SIZE // 2,
                           2)  # рамка

        # Рендерим текст с переносом
        words = self.name.split()
        lines = []
        if len(words) == 1:
            lines.append(self.name)
        else:
            lines.append(words[0])
            lines.append(' '.join(words[1:]))

        y_offset = y + ELEMENT_SIZE // 2 - FONT_SIZE // 2
        for i, line in enumerate(lines):
            text = self.font.render(line, True, BLACK)
            text_rect = text.get_rect(center=(x + ELEMENT_SIZE // 2, y_offset + i * FONT_SIZE))
            surface.blit(text, text_rect)

    def __repr__(self):
        return f"<{self.name}>"


# --- Конкретные элементы (Наследники) ---
class Fire(Element):
    def __init__(self):
        super().__init__("Огонь", "Fire", 1)

    def combine(self, other):
        if isinstance(other, Water):
            return Steam()
        elif isinstance(other, Earth):
            return Lava()
        elif isinstance(other, Air):
            return Life()  # Огонь + Воздух = Жизнь (творческий подход)
        return None


class Water(Element):
    def __init__(self):
        super().__init__("Вода", "Water", 1)

    def combine(self, other):
        if isinstance(other, Fire):
            return Steam()
        elif isinstance(other, Earth):
            return Mud()
        elif isinstance(other, Air):
            return Cloud()
        return None


class Earth(Element):
    def __init__(self):
        super().__init__("Земля", "Earth", 1)

    def combine(self, other):
        if isinstance(other, Fire):
            return Lava()
        elif isinstance(other, Water):
            return Mud()
        elif isinstance(other, Air):
            return Dust()
        return None


class Air(Element):
    def __init__(self):
        super().__init__("Воздух", "Air", 1)

    def combine(self, other):
        if isinstance(other, Fire):
            return Life()
        elif isinstance(other, Water):
            return Cloud()
        elif isinstance(other, Earth):
            return Dust()
        return None


# --- Производные элементы (редкие) ---
class Steam(Element):
    def __init__(self):
        super().__init__("Пар", "Steam", 2)

    def combine(self, other):
        if isinstance(other, Air):
            return Cloud()
        return None


class Mud(Element):
    def __init__(self):
        super().__init__("Грязь", "Mud", 2)

    def combine(self, other):
        if isinstance(other, Fire):
            return Stone()  # Грязь обжигается в камень
        return None


class Lava(Element):
    def __init__(self):
        super().__init__("Лава", "Lava", 2)

    def combine(self, other):
        if isinstance(other, Water):
            return Stone()
        return None


class Cloud(Element):
    def __init__(self):
        super().__init__("Облако", "Cloud", 2)


class Life(Element):
    def __init__(self):
        super().__init__("Жизнь", "Life", 3)


class Dust(Element):
    def __init__(self):
        super().__init__("Пыль", "Dust", 2)


class Stone(Element):
    def __init__(self):
        super().__init__("Камень", "Stone", 2)