import unittest
import os
import sys

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from utils.config import config
from utils.logger import GameLogger


class TestInitialization(unittest.TestCase):
    """Тесты инициализации базовых систем"""

    def test_config_loaded(self):
        """Проверка загрузки конфигурации"""
        self.assertIsNotNone(config)
        self.assertEqual(config.SCREEN_WIDTH, 1200)
        self.assertEqual(config.SCREEN_HEIGHT, 800)

    def test_logger_creation(self):
        """Проверка создания логгера"""
        logger = GameLogger("TestLogger")
        self.assertIsNotNone(logger)

        # Проверяем, что методы логирования существуют
        self.assertTrue(hasattr(logger, 'info'))
        self.assertTrue(hasattr(logger, 'error'))
        self.assertTrue(hasattr(logger, 'warning'))


if __name__ == '__main__':
    unittest.main()