# client/src/core/game_client.py
import requests
import json
from typing import Optional, Dict, Any
from utils.logger import logger
from utils.config import config


class GameClient:
    """Клиент для взаимодействия с сервером игры"""

    def __init__(self):
        self.base_url = config.SERVER_URL
        self.access_token: Optional[str] = None
        self.user_id: Optional[str] = None
        self.session = requests.Session()

    def set_auth_token(self, token: str):
        """Установка токена аутентификации"""
        self.access_token = token
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

    def login(self, username: str, password: str) -> bool:
        """Вход в систему"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/auth/login",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                data = response.json()
                self.set_auth_token(data["access_token"])
                self.user_id = data["user"]["id"]
                logger.info(f"Successfully logged in as {username}")
                return True
            else:
                logger.error(f"Login failed: {response.text}")
                return False

        except requests.RequestException as e:
            logger.error(f"Login request failed: {e}")
            return False

    def register(self, username: str, email: str, password: str, display_name: str = None) -> bool:
        """Регистрация нового пользователя"""
        try:
            payload = {
                "username": username,
                "email": email,
                "password": password
            }
            if display_name:
                payload["display_name"] = display_name

            response = self.session.post(
                f"{self.base_url}/api/v1/auth/register",
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                self.set_auth_token(data["access_token"])
                self.user_id = data["user"]["id"]
                logger.info(f"Successfully registered as {username}")
                return True
            else:
                logger.error(f"Registration failed: {response.text}")
                return False

        except requests.RequestException as e:
            logger.error(f"Registration request failed: {e}")
            return False

    def save_game_progress(self, game_data: Dict[str, Any]) -> bool:
        """Сохранение прогресса игры на сервере"""
        if not self.access_token:
            logger.warning("Cannot save progress - not authenticated")
            return False

        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/game/save-progress",
                json=game_data
            )

            if response.status_code == 200:
                logger.info("Game progress saved successfully")
                return True
            else:
                logger.error(f"Failed to save progress: {response.text}")
                return False

        except requests.RequestException as e:
            logger.error(f"Save progress request failed: {e}")
            return False

    def load_game_progress(self) -> Optional[Dict[str, Any]]:
        """Загрузка прогресса игры с сервера"""
        if not self.access_token:
            logger.warning("Cannot load progress - not authenticated")
            return None

        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/game/load-progress"
            )

            if response.status_code == 200:
                logger.info("Game progress loaded successfully")
                return response.json()
            else:
                logger.error(f"Failed to load progress: {response.text}")
                return None

        except requests.RequestException as e:
            logger.error(f"Load progress request failed: {e}")
            return None

    def get_leaderboard(self, category: str = "wave") -> Optional[list]:
        """Получение таблицы лидеров"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/game/leaderboard",
                params={"category": category}
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get leaderboard: {response.text}")
                return None

        except requests.RequestException as e:
            logger.error(f"Leaderboard request failed: {e}")
            return None

    def visit_player(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Посещение другого игрока"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/social/visit/{player_id}"
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to visit player: {response.text}")
                return None

        except requests.RequestException as e:
            logger.error(f"Visit player request failed: {e}")
            return None