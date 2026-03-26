# game/save_system.py - система сохранений

import json
import os


class SaveSystem:
    """Класс для работы с сохранениями"""

    SAVE_DIR = "assets/data/saves"
    SAVE_PATH = os.path.join(SAVE_DIR, "save.json")

    @classmethod
    def ensure_save_dir(cls):
        """Создаёт папку для сохранений, если её нет"""
        if not os.path.exists(cls.SAVE_DIR):
            os.makedirs(cls.SAVE_DIR)

    @classmethod
    def load_save(cls):
        """Загрузка сохранения"""
        cls.ensure_save_dir()

        default_save = {
            'cups': 0,
            'unlocked_heroes': ['warrior'],
            'selected_hero': 'warrior',
            'wins': 0,
            'losses': 0,
            'achievements': [],
            'settings': {
                'sound_volume': 0.7,
                'music_volume': 0.5,
                'difficulty': 'normal'
            }
        }

        if os.path.exists(cls.SAVE_PATH):
            try:
                with open(cls.SAVE_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Объединяем с дефолтными значениями
                    return {**default_save, **data}
            except (json.JSONDecodeError, IOError):
                return default_save

        return default_save

    @classmethod
    def save_game(cls, data):
        """Сохранение игры"""
        cls.ensure_save_dir()

        try:
            with open(cls.SAVE_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False

    @classmethod
    def add_cups(cls, amount):
        """Добавить кубки"""
        save = cls.load_save()
        save['cups'] += amount
        cls.save_game(save)
        return save['cups']

    @classmethod
    def remove_cups(cls, amount):
        """Удалить кубки"""
        save = cls.load_save()
        save['cups'] = max(0, save['cups'] - amount)
        cls.save_game(save)
        return save['cups']

    @classmethod
    def add_win(cls):
        """Добавить победу"""
        save = cls.load_save()
        save['wins'] += 1
        cls.save_game(save)

    @classmethod
    def add_loss(cls):
        """Добавить поражение"""
        save = cls.load_save()
        save['losses'] += 1
        cls.save_game(save)