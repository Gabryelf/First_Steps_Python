from typing import Dict, List, Any
from datetime import datetime


class Player:
    """Класс для управления данными игрока (не игрового персонажа)"""

    def __init__(self, player_name: str):
        self.player_name = player_name
        self.created_at = datetime.now()
        self.active_hero_name = None
        self.unlocked_heroes = ["Воин", "Маг", "Лучник"]  # Типы героев
        self.statistics = {
            "games_played": 0,
            "games_won": 0,
            "total_enemies_defeated": 0,
            "total_gold_earned": 0,
            "highest_level_reached": 0
        }

    def create_hero(self, hero_name: str, hero_class: str) -> Dict[str, Any]:
        """Создание нового героя для игрока"""
        if hero_class not in self.unlocked_heroes:
            raise ValueError(f"Класс {hero_class} не доступен")

        self.active_hero_name = hero_name
        return {
            "player_name": self.player_name,
            "hero_name": hero_name,
            "hero_class": hero_class,
            "level": 1,
            "experience": 0,
            "gold": 50,
            "created_at": datetime.now(),
            "last_played": datetime.now()
        }

    def update_statistics(self, game_result: Dict[str, Any]):
        """Обновление статистики игрока"""
        self.statistics["games_played"] += 1
        if game_result.get("won"):
            self.statistics["games_won"] += 1
        self.statistics["total_enemies_defeated"] += game_result.get("enemies_defeated", 0)
        self.statistics["total_gold_earned"] += game_result.get("gold_earned", 0)
        self.statistics["highest_level_reached"] = max(
            self.statistics["highest_level_reached"],
            game_result.get("level_reached", 0)
        )