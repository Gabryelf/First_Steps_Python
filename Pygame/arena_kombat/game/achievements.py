# game/achievements.py - система достижений

from arena_kombat.game.save_system import SaveSystem


class Achievement:
    """Класс достижения"""

    def __init__(self, id, name, description, cups_reward, condition_func):
        self.id = id
        self.name = name
        self.description = description
        self.cups_reward = cups_reward
        self.condition_func = condition_func


class AchievementManager:
    """Менеджер достижений"""

    def __init__(self):
        self.achievements = {}
        self.unlocked = []
        self._init_achievements()
        self.load_unlocked()

    def _init_achievements(self):
        """Инициализация всех достижений"""
        self.achievements = {
            'first_win': Achievement(
                'first_win',
                'Первая победа',
                'Одержите первую победу',
                50,
                lambda data: data.get('wins', 0) >= 1
            ),
            'win_3': Achievement(
                'win_3',
                'Серия побед',
                'Одержите 3 победы',
                100,
                lambda data: data.get('wins', 0) >= 3
            ),
            'collector': Achievement(
                'collector',
                'Коллекционер',
                'Откройте второго героя',
                75,
                lambda data: len(data.get('unlocked_heroes', [])) >= 2
            ),
            'perfect_win': Achievement(
                'perfect_win',
                'Идеальная победа',
                'Победите, потеряв менее 10% HP',
                150,
                lambda data: data.get('perfect_win', False)
            )
        }

    def load_unlocked(self):
        """Загрузка открытых достижений"""
        save = SaveSystem.load_save()
        self.unlocked = save.get('achievements', [])

    def check_achievement(self, achievement_id, game_data):
        """Проверка и открытие достижения"""
        if achievement_id in self.unlocked:
            return None

        achievement = self.achievements.get(achievement_id)
        if achievement and achievement.condition_func(game_data):
            self.unlock(achievement_id)
            return achievement

        return None

    def unlock(self, achievement_id):
        """Открыть достижение"""
        achievement = self.achievements.get(achievement_id)
        if achievement and achievement_id not in self.unlocked:
            self.unlocked.append(achievement_id)
            SaveSystem.add_cups(achievement.cups_reward)

            # Сохраняем в файл
            save = SaveSystem.load_save()
            save['achievements'] = self.unlocked
            SaveSystem.save_game(save)

            return True
        return False

    def get_unlocked_percentage(self):
        """Получить процент открытых достижений"""
        if not self.achievements:
            return 0
        return (len(self.unlocked) / len(self.achievements)) * 100