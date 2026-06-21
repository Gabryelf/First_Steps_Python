# !/usr/bin/env python3
"""
Главная точка входа в клиентское приложение Idle Tower Defense
"""

import sys
import os

# Добавляем путь к src в PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from client.src.core.game_engine import GameEngine
    from client.src.utils.logger import logger
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure you have the correct project structure")
    sys.exit(1)


def main():
    """Основная функция запуска игры"""
    logger.info("Starting Idle Tower Defense Client")

    try:
        # Создаем и запускаем игровой движок
        engine = GameEngine()
        engine.run()

    except Exception as e:
        logger.error(f"Critical error in main: {e}")
        print(f"Game crashed with error: {e}")
        return 1

    logger.info("Game exited successfully")
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
