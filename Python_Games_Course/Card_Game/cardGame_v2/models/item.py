from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Any  # Добавляем Any

if TYPE_CHECKING:
    from .hero import Hero


class Item(ABC):
    """Абстрактный класс предмета"""

    def __init__(self, name: str, description: str, value: int, consumable: bool = True):
        self.name = name
        self.description = description
        self.value = value  # Стоимость в золоте
        self.consumable = consumable

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
            "consumable": self.consumable
        }


class HealthPotion(Item):
    """Зелье здоровья"""

    def __init__(self, heal_amount: int = 30):
        super().__init__(
            "Зелье здоровья",
            f"Восстанавливает {heal_amount} здоровья",
            25,
            True
        )
        self.heal_amount = heal_amount

    def use(self, hero: 'Hero') -> str:
        hero.heal(self.heal_amount)
        return f"{hero.name} использует {self.name} и восстанавливает {self.heal_amount} здоровья!"


class EnergyPotion(Item):
    """Зелье энергии"""

    def __init__(self):
        super().__init__("Зелье энергии", "Восстанавливает 2 энергии", 30, True)

    def use(self, hero: 'Hero') -> str:
        hero.energy = min(hero.max_energy, hero.energy + 2)
        return f"{hero.name} использует {self.name} и восстанавливает 2 энергии!"


class PermanentUpgradeItem(Item):
    """Предмет для постоянного улучшения"""

    def __init__(self, name: str, description: str, upgrade_type: str, value: int):
        super().__init__(name, description, value, False)
        self.upgrade_type = upgrade_type

    def use(self, hero: 'Hero') -> str:
        if self.upgrade_type == "health":
            hero.permanent_upgrades["extra_health"] = hero.permanent_upgrades.get("extra_health", 0) + 10
            hero._max_health += 10
            hero._current_health += 10
            return f"{hero.name} увеличил максимальное здоровье на 10!"
        elif self.upgrade_type == "damage":
            hero.permanent_upgrades["extra_damage"] = hero.permanent_upgrades.get("extra_damage", 0) + 2
            return f"{hero.name} увеличил урон на 2!"

        return "Улучшение применено"