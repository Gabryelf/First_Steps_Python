from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Any, List

if TYPE_CHECKING:
    from .hero import Hero


class Item(ABC):
    """Абстрактный класс предмета"""

    def __init__(self, name: str, description: str, value: int, item_type: str, consumable: bool = True):
        self.name = name
        self.description = description
        self.value = value  # Стоимость в золоте
        self.item_type = item_type  # "weapon", "armor", "potion", "relic"
        self.consumable = consumable
        self.equipped = False

    @abstractmethod
    def use(self, hero: 'Hero') -> str:
        """Использование предмета"""
        pass

    def can_use(self, hero: 'Hero') -> bool:
        """Можно ли использовать предмет"""
        return True

    def get_save_data(self) -> Dict[str, Any]:
        """Данные для сохранения"""
        return {
            "name": self.name,
            "description": self.description,
            "value": self.value,
            "item_type": self.item_type,
            "consumable": self.consumable,
            "equipped": self.equipped
        }


# РАСХОДНИКИ
class HealthPotion(Item):
    """Зелье здоровья"""

    def __init__(self, heal_amount: int = 30):
        super().__init__(
            "Зелье здоровья",
            f"Восстанавливает {heal_amount} здоровья",
            25,
            "potion",
            True
        )
        self.heal_amount = heal_amount

    def use(self, hero: 'Hero') -> str:
        hero.heal(self.heal_amount)
        return f"{hero.name} использует {self.name} и восстанавливает {self.heal_amount} здоровья!"


class EnergyPotion(Item):
    """Зелье энергии"""

    def __init__(self):
        super().__init__(
            "Зелье энергии",
            "Восстанавливает 2 энергии",
            30,
            "potion",
            True
        )

    def use(self, hero: 'Hero') -> str:
        old_energy = hero.energy
        hero.energy = min(hero.max_energy, hero.energy + 2)
        gained = hero.energy - old_energy
        return f"{hero.name} использует {self.name} и восстанавливает {gained} энергии!"


class StrengthPotion(Item):
    """Зелье силы (временное усиление)"""

    def __init__(self):
        super().__init__(
            "Зелье силы",
            "Увеличивает урон на 5 до конца боя",
            40,
            "potion",
            True
        )

    def use(self, hero: 'Hero') -> str:
        hero.temporary_buffs["extra_damage"] = hero.temporary_buffs.get("extra_damage", 0) + 5
        return f"{hero.name} использует {self.name}! Урон увеличен на 5 до конца боя."


# ПОСТОЯННЫЕ ПРЕДМЕТЫ
class Weapon(Item):
    """Оружие - увеличивает базовый урон"""

    def __init__(self, name: str, damage_bonus: int, value: int):
        super().__init__(
            name,
            f"Увеличивает урон на {damage_bonus}",
            value,
            "weapon",
            False
        )
        self.damage_bonus = damage_bonus

    def use(self, hero: 'Hero') -> str:
        # Снимаем предыдущее оружие
        for item in hero.inventory:
            if item.item_type == "weapon" and item.equipped:
                item.equipped = False
                hero.equipped_weapon = None

        # Надеваем новое
        self.equipped = True
        hero.equipped_weapon = self
        hero.permanent_upgrades["weapon_damage"] = self.damage_bonus

        return f"{hero.name} экипирует {self.name}! Урон увеличен на {self.damage_bonus}."


class Armor(Item):
    """Броня - увеличивает здоровье"""

    def __init__(self, name: str, health_bonus: int, value: int):
        super().__init__(
            name,
            f"Увеличивает здоровье на {health_bonus}",
            value,
            "armor",
            False
        )
        self.health_bonus = health_bonus

    def use(self, hero: 'Hero') -> str:
        # Снимаем предыдущую броню
        for item in hero.inventory:
            if item.item_type == "armor" and item.equipped:
                item.equipped = False
                hero.equipped_armor = None
                # Убираем бонус здоровья
                hero._max_health -= item.health_bonus
                hero._current_health = min(hero._current_health, hero._max_health)

        # Надеваем новую
        self.equipped = True
        hero.equipped_armor = self
        hero._max_health += self.health_bonus
        hero._current_health += self.health_bonus

        return f"{hero.name} экипирует {self.name}! Здоровье увеличено на {self.health_bonus}."


class Relic(Item):
    """Реаликвия - дает специальные способности"""

    def __init__(self, name: str, description: str, ability: str, value: int):
        super().__init__(name, description, value, "relic", False)
        self.ability = ability

    def use(self, hero: 'Hero') -> str:
        # Снимаем предыдущую реликвию
        for item in hero.inventory:
            if item.item_type == "relic" and item.equipped:
                item.equipped = False
                hero.equipped_relic = None

        # Надеваем новую
        self.equipped = True
        hero.equipped_relic = self

        if self.ability == "extra_energy":
            hero.max_energy += 1
            hero.energy = hero.max_energy

        return f"{hero.name} экипирует {self.name}! {self.description}"