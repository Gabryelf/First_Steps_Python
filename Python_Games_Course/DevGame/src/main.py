"""
Main entry point for the game.
Кроссплатформенная версия.
"""

import sys
import os


# Добавляем корень проекта в Python path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.abspath(project_root))

def main():
    """Инициализация и запуск игры."""
    try:
        from core import GameController
        game = GameController()
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()