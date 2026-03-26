# game.py
import json
import os
from elements import Fire, Water, Earth, Air  # стартовые


class Alchemist:
    """Игрок: управляет инвентарем и рецептами"""

    def __init__(self):
        self.inventory = []  # список объектов Element
        self.discovered_names = set()  # названия открытых элементов (для сохранения)

    def add_element(self, element):
        if element.name not in self.discovered_names:
            self.inventory.append(element)
            self.discovered_names.add(element.name)
            return True
        return False

    def has_element(self, element_name):
        return element_name in self.discovered_names

    def get_element_by_name(self, name):
        for elem in self.inventory:
            if elem.name == name:
                return elem
        return None


class Game:
    """Главный класс игры. Управляет состоянием, сохранением, загрузкой."""

    def __init__(self):
        self.alchemist = Alchemist()
        self.load_or_init()
        self.message = "Смешивай элементы! Перетащи один на другой."
        self.message_timer = 0

    def load_or_init(self):
        """Загружает сохранение или создает начальный инвентарь"""
        save_file = "save.json"
        if os.path.exists(save_file):
            with open(save_file, 'r') as f:
                data = json.load(f)
                # Восстанавливаем объекты элементов по именам
                for elem_name in data.get("inventory", []):
                    elem = self._create_element_by_name(elem_name)
                    if elem:
                        self.alchemist.add_element(elem)
                # Если сохранение пустое или битое, даем стартовые
                if not self.alchemist.inventory:
                    self._give_start_elements()
        else:
            self._give_start_elements()

    def _give_start_elements(self):
        start = [Fire(), Water(), Earth(), Air()]
        for elem in start:
            self.alchemist.add_element(elem)

    def _create_element_by_name(self, name):
        """Фабричный метод: создает объект элемента по имени"""
        # Динамический импорт всех классов из elements
        import elements
        class_map = {
            'Огонь': elements.Fire, 'Вода': elements.Water,
            'Земля': elements.Earth, 'Воздух': elements.Air,
            'Пар': elements.Steam, 'Грязь': elements.Mud,
            'Лава': elements.Lava, 'Облако': elements.Cloud,
            'Жизнь': elements.Life, 'Пыль': elements.Dust,
            'Камень': elements.Stone
        }
        if name in class_map:
            return class_map[name]()
        return None

    def save(self):
        """Сохраняет имена открытых элементов"""
        data = {
            "inventory": list(self.alchemist.discovered_names)
        }
        with open("save.json", 'w') as f:
            json.dump(data, f, indent=2)

    def try_combine(self, elem1, elem2):
        """Пытается объединить два элемента"""
        result = elem1.combine(elem2)
        if result is None:
            # Пробуем в обратном порядке (коммутативность)
            result = elem2.combine(elem1)

        if result:
            if self.alchemist.add_element(result):
                self.message = f"Открыт новый элемент: {result.name}!"
                self.message_timer = 120  # кадров
                self.save()
                return result
            else:
                self.message = f"Элемент {result.name} уже есть в коллекции."
                self.message_timer = 60
                return None
        else:
            self.message = "Ничего не произошло."
            self.message_timer = 60
            return None

    def update_message(self):
        if self.message_timer > 0:
            self.message_timer -= 1
        else:
            self.message = ""