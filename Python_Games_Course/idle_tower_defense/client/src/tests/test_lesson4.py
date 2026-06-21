import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from database.base_database import MockDatabase
from systems.upgrade_system import UpgradeSystem, Upgrade
from entities.tower import Tower


class TestLesson4(unittest.TestCase):

    def test_mock_database_operations(self):
        """Тест операций с mock базой данных"""
        db = MockDatabase()
        db.connect()

        # Тест сохранения и загрузки
        test_data = {'high_score': 1000, 'level': 5}
        self.assertTrue(db.save_player_data('test_player', test_data))

        loaded_data = db.load_player_data('test_player')
        self.assertEqual(loaded_data['high_score'], 1000)

        db.disconnect()

    def test_upgrade_system_initialization(self):
        """Тест инициализации системы улучшений"""
        upgrade_system = UpgradeSystem()
        self.assertEqual(len(upgrade_system.available_upgrades), 5)
        self.assertIn('damage', upgrade_system.available_upgrades)

    def test_upgrade_cost_calculation(self):
        """Тест расчета стоимости улучшений"""
        upgrade_system = UpgradeSystem()
        tower = Tower()

        # Первый уровень должен стоить базовую цену
        first_cost = upgrade_system.get_upgrade_cost('damage')
        self.assertEqual(first_cost, 50)  # 50 * 1

        # Применяем улучшение и проверяем увеличение стоимости
        from core.game_state import GameState, PlayerProgress
        game_state = GameState()

        success, message = upgrade_system.apply_upgrade('damage', tower, game_state)
        self.assertTrue(success)

        second_cost = upgrade_system.get_upgrade_cost('damage')
        self.assertEqual(second_cost, 100)  # 50 * 2


if __name__ == '__main__':
    unittest.main()