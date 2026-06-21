#!/usr/bin/env python3
"""
Тестовый скрипт для проверки спавна врагов
"""

import sys
import os

# Добавляем путь к src
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.enemy_spawner import EnemySpawner
from utils.config import config
from utils.logger import logger


def test_spawner():
    """Тестирование спавнера врагов"""
    logger.info("Testing enemy spawner...")

    spawner = EnemySpawner()

    print("🔍 Testing spawn positions:")
    for i in range(10):
        pos = spawner.get_random_spawn_position()
        print(f"  {i + 1}. {pos}")

    print(f"📏 Screen size: {config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}")
    print("✅ Spawner test completed")


if __name__ == "__main__":
    test_spawner()