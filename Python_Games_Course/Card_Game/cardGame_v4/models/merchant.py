from typing import List
from .item import HealthPotion, EnergyPotion, StrengthPotion, Weapon, Armor, Relic
import random


class Merchant:
    """Класс торговца"""

    def __init__(self, level: int = 1):
        self.level = level
        self.inventory: List = []
        self._generate_inventory()

    def _generate_inventory(self):
        """Генерация инвентаря торговца"""
        # Всегда есть зелья
        self.inventory.extend([
            HealthPotion(),
            EnergyPotion(),
            StrengthPotion()
        ])

        # Оружие и броня в зависимости от уровня
        if self.level >= 2:
            self.inventory.extend([
                Weapon("Стальной меч", 3, 100),
                Armor("Кожаный доспех", 15, 80)
            ])

        if self.level >= 3:
            self.inventory.extend([
                Weapon("Мифрильный клинок", 5, 200),
                Armor("Кольчуга", 25, 150)
            ])

    def get_items_for_sale(self):
        """Получить предметы для продажи"""
        return self.inventory

    def buy_item(self, hero, item_index: int) -> str:
        """Покупка предмета героем"""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]

            if hero.gold >= item.value:
                hero.gold -= item.value
                hero.inventory.append(item)
                self.inventory.pop(item_index)
                return f"Куплено: {item.name} за {item.value} золота!"
            else:
                return "Недостаточно золота!"
        return "Неверный индекс предмета"