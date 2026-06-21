from dataclasses import dataclass
from typing import Dict, List, Tuple
import random
from client.src.utils.logger import logger


@dataclass
class WaveConfig:
    """Конфигурация отдельной волны"""
    wave_number: int
    total_enemies: int
    enemy_types: List[str]
    spawn_interval: float  # Интервал между спавном врагов
    enemy_health_multiplier: float = 1.0
    enemy_speed_multiplier: float = 1.0


class WaveConfigManager:
    """Менеджер конфигурации волн"""

    def __init__(self):
        self.wave_configs: Dict[int, WaveConfig] = {}
        self._initialize_wave_configs()
        logger.info("WaveConfigManager initialized")

    def _initialize_wave_configs(self):
        """Инициализация конфигураций волн"""
        # Волна 1
        self.wave_configs[1] = WaveConfig(
            wave_number=1,
            total_enemies=10,
            enemy_types=["goblin", "goblin", "goblin"],  # 70% гоблинов, 30% орков
            spawn_interval=2.0,
            enemy_health_multiplier=1.0,
            enemy_speed_multiplier=1.0
        )

        # Волна 2
        self.wave_configs[2] = WaveConfig(
            wave_number=2,
            total_enemies=15,
            enemy_types=["goblin", "goblin", "orc"],
            spawn_interval=1.8,
            enemy_health_multiplier=1.2,
            enemy_speed_multiplier=1.1
        )

        # Волна 3
        self.wave_configs[3] = WaveConfig(
            wave_number=3,
            total_enemies=20,
            enemy_types=["goblin", "orc", "orc"],
            spawn_interval=1.5,
            enemy_health_multiplier=1.4,
            enemy_speed_multiplier=1.2
        )

        # Волна 4-10 - генерируем автоматически
        for wave in range(4, 11):
            self.wave_configs[wave] = WaveConfig(
                wave_number=wave,
                total_enemies=15 + wave * 3,
                enemy_types=self._get_enemy_types_for_wave(wave),
                spawn_interval=max(0.5, 2.0 - wave * 0.1),
                enemy_health_multiplier=1.0 + wave * 0.2,
                enemy_speed_multiplier=1.0 + wave * 0.1
            )

    def _get_enemy_types_for_wave(self, wave: int) -> List[str]:
        """Получение типов врагов для волны"""
        if wave <= 3:
            return ["goblin", "goblin", "orc"]
        elif wave <= 6:
            return ["goblin", "orc", "orc"]
        elif wave <= 9:
            return ["orc", "orc", "boss"] if wave % 3 == 0 else ["goblin", "orc", "orc"]
        else:
            return ["orc", "boss", "boss"] if wave % 2 == 0 else ["goblin", "orc", "boss"]

    def get_wave_config(self, wave_number: int) -> WaveConfig:
        """Получение конфигурации волны"""
        if wave_number in self.wave_configs:
            return self.wave_configs[wave_number]
        else:
            # Генерация конфигурации для волн выше 10
            return WaveConfig(
                wave_number=wave_number,
                total_enemies=15 + wave_number * 3,
                enemy_types=self._get_enemy_types_for_wave(wave_number),
                spawn_interval=max(0.3, 2.0 - wave_number * 0.1),
                enemy_health_multiplier=1.0 + wave_number * 0.2,
                enemy_speed_multiplier=1.0 + wave_number * 0.1
            )

    def get_random_enemy_type(self, wave_number: int) -> str:
        """Получение случайного типа врага для волны"""
        config = self.get_wave_config(wave_number)
        return random.choice(config.enemy_types)