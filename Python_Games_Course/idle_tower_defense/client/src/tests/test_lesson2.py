import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from core.game_state import GameState, GameStateType, PlayerProgress
from entities.tower import Tower, TowerStats
from core.wave_manager import WaveManager


class TestLesson2(unittest.TestCase):

    def test_game_state_initialization(self):
        """Тест инициализации состояния игры"""
        state = GameState()
        self.assertEqual(state.current_state, GameStateType.LOBBY)
        self.assertIsInstance(state.player_progress, PlayerProgress)

    def test_player_progress_operations(self):
        """Тест операций с прогрессом игрока"""
        progress = PlayerProgress()
        progress.add_coins(50)
        self.assertEqual(progress.coins, 150)

        self.assertTrue(progress.spend_coins(50))
        self.assertEqual(progress.coins, 100)

        self.assertFalse(progress.spend_coins(200))
        self.assertEqual(progress.coins, 100)

    def test_tower_creation(self):
        """Тест создания башни"""
        tower = Tower()
        self.assertEqual(tower.level, 1)
        self.assertEqual(tower.experience, 0)
        self.assertIsInstance(tower.current_stats, TowerStats)

    def test_wave_manager(self):
        """Тест менеджера волн"""
        wave_manager = WaveManager()
        wave_manager.start_wave(3)
        self.assertEqual(wave_manager.current_wave, 3)
        self.assertTrue(wave_manager.wave_in_progress)


if __name__ == '__main__':
    unittest.main()