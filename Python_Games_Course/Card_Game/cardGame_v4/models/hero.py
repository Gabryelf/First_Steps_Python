from typing import List, Dict, Any, Optional  # Добавляем Optional
from .entity import Entity
from .card import Card
from .item import Item
import math


class Hero(Entity):
    """Расширенный класс героя с прогрессией"""

    def __init__(self, name: str, hero_class: str, max_health: int = 100):
        super().__init__(name, max_health)
        self.hero_class = hero_class
        self.level = 1
        self.experience = 0
        self.gold = 50  # Стартовое золото
        self.energy = 3
        self.max_energy = 3
        self._deck: List[Card] = []
        self._hand: List[Card] = []
        self.inventory: List[Item] = []
        self.permanent_upgrades: Dict[str, Any] = {}
        self.temporary_buffs: Dict[str, Any] = {}  # Временные усиления

        # Экипированные предметы - теперь с правильными аннотациями
        self.equipped_weapon: Optional[Item] = None
        self.equipped_armor: Optional[Item] = None
        self.equipped_relic: Optional[Item] = None

        self._initialize_class(hero_class)
        self._add_starting_items()

    def _initialize_class(self, hero_class: str):
        """Инициализация стартовых карт в зависимости от класса"""
        from .attack_card import AttackCard
        from .defense_card import DefenseCard

        if hero_class == "Воин":
            self._deck.extend([
                AttackCard("Удар мечом", 10, 1),
                AttackCard("Сильный удар", 15, 2),
                DefenseCard("Блок", 8, 1)
            ])
            self.permanent_upgrades["extra_health"] = 20
        elif hero_class == "Маг":
            self._deck.extend([
                AttackCard("Магическая стрела", 8, 1),
                AttackCard("Огненный шар", 20, 3),
                DefenseCard("Магический щит", 5, 1)
            ])
            self.permanent_upgrades["extra_energy"] = 1
        elif hero_class == "Лучник":
            self._deck.extend([
                AttackCard("Выстрел", 12, 1),
                AttackCard("Меткий выстрел", 18, 2),
                AttackCard("Дождь стрел", 25, 3)
            ])
            self.permanent_upgrades["extra_damage"] = 3

        self._apply_permanent_upgrades()

    def _apply_permanent_upgrades(self):
        """Применение постоянных улучшений"""
        if "extra_health" in self.permanent_upgrades:
            self._max_health += self.permanent_upgrades["extra_health"]
            self._current_health = self._max_health
        if "extra_energy" in self.permanent_upgrades:
            self.max_energy += self.permanent_upgrades["extra_energy"]
            self.energy = self.max_energy

    def get_available_actions(self) -> List[str]:
        actions = ["закончить ход"]
        if any(card.energy_cost <= self.energy for card in self._hand):
            actions.append("использовать карту")
        if any(item.can_use(self) for item in self.inventory):
            actions.append("использовать предмет")
        return actions

    def add_card_to_deck(self, card: Card):
        """Добавить карту в колоду"""
        self._deck.append(card)

    def draw_hand(self, cards_count: int = 5):
        """Взять карты в руку (упрощенная версия)"""
        # Берем карты из колоды, если их достаточно
        if len(self._deck) >= cards_count:
            self._hand = self._deck[:cards_count]
        else:
            # Если карт в колоде меньше, берем все что есть
            self._hand = self._deck.copy()

    def get_hand(self) -> List[Card]:
        """Получить карты в руке"""
        return self._hand.copy()

    def play_card(self, card_index: int, target: 'Entity' = None) -> str:
        """Сыграть карту из руки"""
        if 0 <= card_index < len(self._hand):
            card = self._hand[card_index]
            if self.energy >= card.energy_cost:
                self.energy -= card.energy_cost
                result = card.play(self, target)
                # Убираем карту из руки
                self._hand.pop(card_index)
                return result
            return "Недостаточно энергии!"
        return "Неверный индекс карты!"

    def start_turn(self):
        """Начало хода героя - восстановление энергии"""
        self.energy = self.max_energy  # Полное восстановление каждый ход
        self.draw_hand()

    def level_up(self):
        """Повышение уровня героя"""
        self.level += 1
        self.experience = max(0, self.experience - self._get_required_experience())

        # Базовая прокачка
        self._max_health += 10
        self._current_health = self._max_health
        self.max_energy = max(self.max_energy, 3 + self.level // 3)
        self.energy = self.max_energy  # Восстанавливаем энергию при level up

        return f"{self.name} достиг {self.level} уровня! +10 к здоровью, +1 к макс. энергии"

    def add_experience(self, exp: int):
        """Добавление опыта и проверка уровня"""
        self.experience += exp
        required_exp = self._get_required_experience()

        while self.experience >= required_exp:
            level_up_message = self.level_up()
            # Можно добавить сообщение в лог если нужно
            required_exp = self._get_required_experience()

    def _get_required_experience(self) -> int:
        """Формула требуемого опыта для следующего уровня"""
        return 100 * self.level + 50 * (self.level - 1) ** 1.5

    def add_gold(self, amount: int):
        """Добавление золота"""
        self.gold += amount

    def add_item(self, item: Item):
        """Добавление предмета в инвентарь"""
        self.inventory.append(item)

    def _add_starting_items(self):
        """Добавляем стартовые предметы"""
        from .item import HealthPotion
        self.inventory.append(HealthPotion())
        self.inventory.append(HealthPotion())

    def use_item(self, item_index: int) -> str:
        """Использование предмета из инвентаря"""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            if item.can_use(self):
                result = item.use(self)

                # Если предмет расходуемый - удаляем из инвентаря
                if item.consumable:
                    self.inventory.pop(item_index)

                return result
            return "Нельзя использовать этот предмет"
        return "Неверный индекс предмета"

    def get_equipped_items(self) -> List[Item]:
        """Получить список экипированных предметов"""
        equipped = []
        if self.equipped_weapon:
            equipped.append(self.equipped_weapon)
        if self.equipped_armor:
            equipped.append(self.equipped_armor)
        if self.equipped_relic:
            equipped.append(self.equipped_relic)
        return equipped

    def calculate_damage(self, base_damage: int) -> int:
        """Рассчет урона с учетом предметов и баффов"""
        total_damage = base_damage

        # Бонус от оружия
        if self.equipped_weapon and hasattr(self.equipped_weapon, 'damage_bonus'):
            total_damage += self.equipped_weapon.damage_bonus

        # Временные баффы (от зелий)
        total_damage += self.temporary_buffs.get("extra_damage", 0)

        # Постоянные улучшения
        total_damage += self.permanent_upgrades.get("extra_damage", 0)

        return total_damage

    def start_battle(self):
        """Начало битвы - сбрасываем временные баффы"""
        self.temporary_buffs.clear()

    def end_battle(self):
        """Конец битвы - сбрасываем временные баффы от зелий"""
        if "extra_damage" in self.temporary_buffs:
            del self.temporary_buffs["extra_damage"]

    def get_save_data(self) -> Dict[str, Any]:
        """Получение данных для сохранения"""
        return {
            "name": self.name,
            "hero_class": self.hero_class,
            "level": self.level,
            "experience": self.experience,
            "gold": self.gold,
            "max_health": self._max_health,
            "current_health": self._current_health,
            "permanent_upgrades": self.permanent_upgrades,
            "inventory": [item.get_save_data() for item in self.inventory],
            "equipped_weapon": self.equipped_weapon.get_save_data() if self.equipped_weapon else None,
            "equipped_armor": self.equipped_armor.get_save_data() if self.equipped_armor else None,
            "equipped_relic": self.equipped_relic.get_save_data() if self.equipped_relic else None
        }

    def can_equip_item(self, item: Item) -> bool:
        """Можно ли экипировать предмет"""
        if item.item_type == "weapon":
            return True
        elif item.item_type == "armor":
            return True
        elif item.item_type == "relic":
            return True
        return False

    def get_equipped_item_of_type(self, item_type: str) -> Optional[Item]:
        """Получить экипированный предмет определенного типа"""
        if item_type == "weapon":
            return self.equipped_weapon
        elif item_type == "armor":
            return self.equipped_armor
        elif item_type == "relic":
            return self.equipped_relic
        return None