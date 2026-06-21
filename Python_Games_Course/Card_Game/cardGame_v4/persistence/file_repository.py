import json
import os
from typing import Optional, Dict, Any, List
from datetime import datetime


class FileGameRepository:
    """Репозиторий для сохранения в файлы JSON"""

    def __init__(self, save_dir: str = "saves"):
        self.save_dir = save_dir
        self.players_file = os.path.join(save_dir, "players.json")
        self.saves_file = os.path.join(save_dir, "saves.json")
        self.leaderboard_file = os.path.join(save_dir, "leaderboard.json")

        # Создаем папку если не существует
        os.makedirs(save_dir, exist_ok=True)

        # Загружаем данные
        self.players_data = self._load_json(self.players_file, {})
        self.saves_data = self._load_json(self.saves_file, {})
        self.leaderboard_data = self._load_json(self.leaderboard_file, [])

        print(f"Инициализирован файловый репозиторий в папке {save_dir}")

    def _load_json(self, filepath: str, default):
        """Загрузка данных из JSON файла"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки {filepath}: {e}")
        return default

    def _save_json(self, filepath: str, data):
        """Сохранение данных в JSON файл"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            print(f"Ошибка сохранения {filepath}: {e}")
            return False

    def save_game(self, player_name: str, hero_data: Dict[str, Any], game_state: Dict[str, Any]) -> str:
        """Сохранить игру в файл"""
        save_key = f"{player_name}_{hero_data['name']}"

        save_data = {
            "player_name": player_name,
            "hero_name": hero_data["name"],
            "hero_data": hero_data,
            "game_state": game_state,
            "last_saved": datetime.now().isoformat(),
            "level": hero_data.get("level", 1)
        }

        # Обновляем в памяти
        if player_name in self.players_data:
            self.players_data[player_name]["active_hero"] = hero_data["name"]

        self.saves_data[save_key] = save_data

        # Сохраняем в файлы
        self._save_json(self.players_file, self.players_data)
        self._save_json(self.saves_file, self.saves_data)

        print(f"Игра сохранена в файл: {player_name} - {hero_data['name']}")
        return f"Игра сохранена для {player_name} - {hero_data['name']}"

    def create_player(self, player_name: str) -> bool:
        """Создание нового игрока"""
        if player_name in self.players_data:
            return False  # Игрок уже существует

        player_data = {
            "player_name": player_name,
            "created_at": datetime.now(),
            "active_hero": None,
            "statistics": {
                "games_played": 0,
                "games_won": 0,
                "total_enemies_defeated": 0,
                "total_gold_earned": 0,
                "highest_level_reached": 0
            }
        }

        self.players_data[player_name] = player_data
        print(f"Создан игрок: {player_name}")
        return True

    def get_player(self, player_name: str) -> Optional[Dict[str, Any]]:
        """Получение данных игрока"""
        return self.players_data.get(player_name)


    def load_game(self, player_name: str, hero_name: str) -> Optional[Dict[str, Any]]:
        """Загрузить игру"""
        save_key = f"{player_name}_{hero_name}"
        return self.saves_data.get(save_key)

    def get_player_saves(self, player_name: str) -> List[Dict[str, Any]]:
        """Получить все сохранения игрока"""
        saves = []
        for save_key, save_data in self.saves_data.items():
            if save_data["player_name"] == player_name:
                saves.append({
                    "hero_name": save_data["hero_name"],
                    "level": save_data.get("level", 1),
                    "last_saved": save_data.get("last_saved")
                })
        return saves

    def update_leaderboard(self, player_name: str, hero_name: str, score_data: Dict[str, Any]):
        """Обновление таблицы лидеров"""
        leaderboard_entry = {
            "player_name": player_name,
            "hero_name": hero_name,
            "level": score_data.get("level", 1),
            "score": score_data.get("score", 0),
            "enemies_defeated": score_data.get("enemies_defeated", 0),
            "gold_collected": score_data.get("gold_collected", 0),
            "last_updated": datetime.now()
        }

        # Удаляем старую запись если есть
        self.leaderboard_data = [entry for entry in self.leaderboard_data
                                 if not (entry["player_name"] == player_name and
                                         entry["hero_name"] == hero_name)]

        # Добавляем новую
        self.leaderboard_data.append(leaderboard_entry)

        # Сортируем по очкам
        self.leaderboard_data.sort(key=lambda x: x["score"], reverse=True)

        print(f"Обновлен лидерборд: {player_name} - {score_data.get('score', 0)} очков")

    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Получить таблицу лидеров"""
        return self.leaderboard_data[:limit]

    def update_player_statistics(self, player_name: str, game_result: Dict[str, Any]):
        """Обновление статистики игрока"""
        if player_name not in self.players_data:
            return

        player_data = self.players_data[player_name]
        stats = player_data["statistics"]

        stats["games_played"] += 1
        stats["total_enemies_defeated"] += game_result.get("enemies_defeated", 0)
        stats["total_gold_earned"] += game_result.get("gold_earned", 0)

        if game_result.get("won"):
            stats["games_won"] += 1

        if game_result.get("level_reached", 0) > 0:
            stats["highest_level_reached"] = max(
                stats["highest_level_reached"],
                game_result.get("level_reached", 0)
            )

        print(f"Обновлена статистика игрока {player_name}")