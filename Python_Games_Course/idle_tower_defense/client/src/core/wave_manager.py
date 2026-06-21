from typing import List, Dict, Any
import random
from client.src.utils.logger import logger
from .wave_config import WaveConfigManager


class WaveManager:
    """Менеджер волн врагов"""

    def __init__(self):
        self.current_wave = 0
        self.wave_config_manager = WaveConfigManager()
        self.wave_in_progress = False
        self.enemies_spawned = 0
        self.enemies_defeated = 0
        self.spawn_timer = 0

        logger.info("WaveManager initialized")

    def start_wave(self, wave_number: int):
        """Начать волну"""
        self.current_wave = wave_number
        wave_config = self.wave_config_manager.get_wave_config(wave_number)

        self.enemies_spawned = 0
        self.enemies_defeated = 0
        self.wave_in_progress = True
        self.spawn_timer = 0

        logger.info(f"Wave {wave_number} started. Enemies: {wave_config.total_enemies}")

    def update(self, delta_time: float, game_state) -> List[str]:
        """Обновление логики волны"""
        enemies_to_spawn = []

        # Если волна не идет, начинаем следующую
        if not self.wave_in_progress:
            next_wave = self.current_wave + 1 if self.current_wave > 0 else 1
            self.start_wave(next_wave)
            logger.info(f"Auto-starting wave {next_wave}")
            return enemies_to_spawn

        wave_config = self.wave_config_manager.get_wave_config(self.current_wave)
        self.spawn_timer += delta_time

        # Спавн новых врагов
        if (self.spawn_timer >= wave_config.spawn_interval and
                self.enemies_spawned < wave_config.total_enemies):
            enemy_type = self.wave_config_manager.get_random_enemy_type(self.current_wave)
            enemies_to_spawn.append(enemy_type)
            self.enemies_spawned += 1
            self.spawn_timer = 0

            logger.info(f"Spawning {enemy_type}. Progress: {self.enemies_spawned}/{wave_config.total_enemies}")

        # Проверка завершения волны
        if (self.enemies_spawned >= wave_config.total_enemies and
                self.enemies_defeated >= wave_config.total_enemies):
            self._complete_wave(game_state)

        return enemies_to_spawn

    def _complete_wave(self, game_state):
        """Завершение волны"""
        self.wave_in_progress = False
        game_state.player_progress.current_wave += 1

        # Награда за завершение волны
        reward = self.current_wave * 15
        game_state.player_progress.add_coins(reward)

        logger.info(f"Wave {self.current_wave} completed! Reward: {reward} coins")

    def on_enemy_defeated(self):
        """Вызывается при победе над врагом"""
        self.enemies_defeated += 1
        wave_config = self.wave_config_manager.get_wave_config(self.current_wave)
        logger.debug(f"Enemy defeated. Total: {self.enemies_defeated}/{wave_config.total_enemies}")