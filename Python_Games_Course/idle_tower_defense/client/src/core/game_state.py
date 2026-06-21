from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, Any, List
from client.src.utils.logger import logger


class GameStateType(Enum):
    """Типы состояний игры"""
    LOBBY = auto()  # Лобби - экран входа
    BATTLE = auto()  # Битва - основной игровой процесс
    UPGRADE = auto()  # Магазин улучшений
    GAME_OVER = auto()  # Конец игры


@dataclass
class PlayerProgress:
    """Прогресс игрока в рамках одной сессии"""
    coins: int = 100
    diamonds: int = 0
    score: int = 0
    current_wave: int = 1
    enemies_defeated: int = 0

    def add_coins(self, amount: int):
        """Добавить монеты"""
        self.coins += amount
        logger.debug(f"Added {amount} coins. Total: {self.coins}")

    def spend_coins(self, amount: int) -> bool:
        """Потратить монеты (если достаточно)"""
        if self.coins >= amount:
            self.coins -= amount
            logger.debug(f"Spent {amount} coins. Remaining: {self.coins}")
            return True
        return False


class GameState:
    """Основное состояние игры - центральный класс для всей игровой логики"""

    def __init__(self):
        self.current_state = GameStateType.LOBBY
        self.player_progress = PlayerProgress()
        self.game_active = False
        self.wave_in_progress = False
        self.victory = False

        # Статистика текущей битвы
        self.current_enemies: List['Enemy'] = []
        self.tower = None

        logger.info("GameState initialized")

    def change_state(self, new_state: GameStateType):
        """Смена состояния игры"""
        old_state = self.current_state
        self.current_state = new_state
        logger.info(f"Game state changed: {old_state.name} -> {new_state.name}")

    def start_battle(self):
        """Начать новую битву"""
        if self.current_state == GameStateType.LOBBY:
            self.change_state(GameStateType.BATTLE)
            self.game_active = True
            self.victory = False
            self.player_progress = PlayerProgress()  # Сброс прогресса для новой битвы
            logger.info("New battle started")

    def end_battle(self, victory: bool):
        """Завершить битву"""
        self.victory = victory
        self.game_active = False

        if victory:
            # Награда за победу
            reward = self.player_progress.current_wave * 10
            self.player_progress.add_coins(reward)
            self.player_progress.diamonds += 1
            logger.info(f"Battle victorious! Reward: {reward} coins, 1 diamond")
        else:
            logger.info("Battle lost - tower destroyed")

        self.change_state(GameStateType.LOBBY)