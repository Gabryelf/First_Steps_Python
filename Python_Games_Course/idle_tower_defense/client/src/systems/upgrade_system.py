from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from client.src.entities.tower import Tower, TowerStats
from client.src.utils.logger import logger


@dataclass
class Upgrade:
    """Класс улучшения башни"""
    name: str
    description: str
    cost: int
    stat: str  # damage, attack_speed, attack_range, critical_chance, critical_multiplier
    value: float
    max_level: int = 10


class UpgradeSystem:
    """Система улучшений башни"""

    def __init__(self):
        self.available_upgrades: Dict[str, Upgrade] = {}
        self.player_upgrades: Dict[str, int] = {}  # upgrade_name -> current_level
        self._initialize_upgrades()

        logger.info("UpgradeSystem initialized")

    def _initialize_upgrades(self):
        """Инициализация доступных улучшений"""
        self.available_upgrades = {
            "damage": Upgrade(
                name="Урон",
                description="Увеличивает урон башни",
                cost=50,
                stat="damage",
                value=1.2,  # +20% за уровень
                max_level=20
            ),
            "attack_speed": Upgrade(
                name="Скорость атаки",
                description="Увеличивает скорость атаки",
                cost=75,
                stat="attack_speed",
                value=1.15,  # +15% за уровень
                max_level=15
            ),
            "attack_range": Upgrade(
                name="Дальность",
                description="Увеличивает радиус атаки",
                cost=100,
                stat="attack_range",
                value=1.1,  # +10% за уровень
                max_level=10
            ),
            "critical_chance": Upgrade(
                name="Шанс крита",
                description="Увеличивает шанс критического удара",
                cost=150,
                stat="critical_chance",
                value=0.05,  # +5% за уровень
                max_level=5
            ),
            "critical_multiplier": Upgrade(
                name="Множитель крита",
                description="Увеличивает урон критического удара",
                cost=200,
                stat="critical_multiplier",
                value=0.3,  # +30% за уровень
                max_level=3
            )
        }

        # Инициализация уровней улучшений
        for upgrade_name in self.available_upgrades:
            self.player_upgrades[upgrade_name] = 0

    def can_upgrade(self, upgrade_name: str, current_coins: int) -> Tuple[bool, str]:
        """Проверка возможности улучшения"""
        if upgrade_name not in self.available_upgrades:
            return False, "Улучшение не найдено"

        upgrade = self.available_upgrades[upgrade_name]
        current_level = self.player_upgrades[upgrade_name]

        if current_level >= upgrade.max_level:
            return False, "Максимальный уровень достигнут"

        upgrade_cost = self.get_upgrade_cost(upgrade_name)
        if current_coins < upgrade_cost:
            return False, "Недостаточно монет"

        return True, "Можно улучшить"

    def get_upgrade_cost(self, upgrade_name: str) -> int:
        """Получение стоимости улучшения"""
        if upgrade_name not in self.available_upgrades:
            return 0

        upgrade = self.available_upgrades[upgrade_name]
        current_level = self.player_upgrades[upgrade_name]

        # Стоимость увеличивается с каждым уровнем
        return upgrade.cost * (current_level + 1)

    def apply_upgrade(self, upgrade_name: str, tower: Tower, game_state) -> Tuple[bool, str]:
        """Применение улучшения к башне"""
        can_upgrade, message = self.can_upgrade(upgrade_name, game_state.player_progress.coins)
        if not can_upgrade:
            return False, message

        upgrade = self.available_upgrades[upgrade_name]
        upgrade_cost = self.get_upgrade_cost(upgrade_name)

        # Списание монет
        if not game_state.player_progress.spend_coins(upgrade_cost):
            return False, "Не удалось списать монеты"

        # Увеличение уровня улучшения
        self.player_upgrades[upgrade_name] += 1

        # Применение улучшения к статистике башни
        self._apply_upgrade_to_tower(upgrade, tower)

        logger.info(f"Upgrade applied: {upgrade_name} to level {self.player_upgrades[upgrade_name]}")
        return True, f"{upgrade.name} улучшено до уровня {self.player_upgrades[upgrade_name]}"

    def _apply_upgrade_to_tower(self, upgrade: Upgrade, tower: Tower):
        """Применение улучшения к статистике башни"""
        if upgrade.stat == "damage":
            tower.current_stats.damage *= upgrade.value
        elif upgrade.stat == "attack_speed":
            tower.current_stats.attack_speed *= upgrade.value
        elif upgrade.stat == "attack_range":
            tower.current_stats.attack_range *= upgrade.value
        elif upgrade.stat == "critical_chance":
            tower.current_stats.critical_chance += upgrade.value
        elif upgrade.stat == "critical_multiplier":
            tower.current_stats.critical_multiplier += upgrade.value

    def get_upgrade_info(self, upgrade_name: str) -> Dict[str, any]:
        """Получение информации об улучшении"""
        if upgrade_name not in self.available_upgrades:
            return {}

        upgrade = self.available_upgrades[upgrade_name]
        current_level = self.player_upgrades[upgrade_name]

        return {
            'name': upgrade.name,
            'description': upgrade.description,
            'current_level': current_level,
            'max_level': upgrade.max_level,
            'next_cost': self.get_upgrade_cost(upgrade_name),
            'can_upgrade': current_level < upgrade.max_level
        }

    def get_all_upgrades_info(self) -> Dict[str, Dict[str, any]]:
        """Получение информации о всех улучшениях"""
        return {name: self.get_upgrade_info(name) for name in self.available_upgrades}

    def save_upgrades(self) -> Dict[str, int]:
        """Сохранение текущих улучшений"""
        return self.player_upgrades.copy()

    def load_upgrades(self, upgrades_data: Dict[str, int]):
        """Загрузка улучшений"""
        for upgrade_name, level in upgrades_data.items():
            if upgrade_name in self.player_upgrades:
                self.player_upgrades[upgrade_name] = level