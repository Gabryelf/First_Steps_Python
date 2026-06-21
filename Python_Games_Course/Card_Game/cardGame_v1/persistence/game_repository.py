from pymongo import MongoClient
from typing import Optional, Dict, Any
import json


class GameRepository:
    """Реpository для работы с сохранениями в MongoDB"""

    def __init__(self, connection_string: str = "mongodb://localhost:27017/"):
        self.client = MongoClient(connection_string)
        self.db = self.client.card_roguelike
        self.saves = self.db.saves

    def save_game(self, hero_name: str, game_data: Dict[str, Any]) -> str:
        """Сохранить игру"""
        save_data = {
            "hero_name": hero_name,
            "game_data": game_data,
            "timestamp": json.dumps(game_data, default=str)  # Для простоты сериализуем в JSON
        }

        result = self.saves.replace_one(
            {"hero_name": hero_name},
            save_data,
            upsert=True
        )

        return f"Игра сохранена для героя {hero_name}"

    def load_game(self, hero_name: str) -> Optional[Dict[str, Any]]:
        """Загрузить игру"""
        save_data = self.saves.find_one({"hero_name": hero_name})
        if save_data:
            return save_data.get("game_data")
        return None

    def get_save_list(self) -> list:
        """Получить список сохранений"""
        return list(self.saves.find({}, {"hero_name": 1, "timestamp": 1}))