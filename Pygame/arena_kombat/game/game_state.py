# game/game_state.py - управление состояниями игры

import pygame
from arena_kombat.config.settings import *
from arena_kombat.game.menu import MainMenu, HeroSelectMenu, SettingsMenu
from arena_kombat.game.arena import Arena
from arena_kombat.game.save_system import SaveSystem
from arena_kombat.characters.warrior import Warrior
from arena_kombat.characters.mage import Mage
from arena_kombat.characters.archer import Archer


class GameState:
    """Управляет текущим состоянием игры (меню, бой)"""

    def __init__(self, screen):
        self.screen = screen
        self.state = 'menu'  # menu, hero_select, settings, battle
        self.menu = MainMenu(screen)
        self.hero_select = None
        self.settings_menu = SettingsMenu(screen)
        self.arena = None
        self.save_data = SaveSystem.load_save()

        # Словарь для создания героев по ID
        self.heroes = {
            'warrior': Warrior,
            'mage': Mage,
            'archer': Archer
        }

        self.selected_hero = self.save_data['selected_hero']

    def handle_event(self, event):
        """Обработка событий в зависимости от состояния"""
        if self.state == 'menu':
            action = self.menu.handle_event(event)
            if action == 'start':
                # Начать бой с выбранным героем
                self.start_battle()
            elif action == 'hero_select':
                self.state = 'hero_select'
                self.hero_select = HeroSelectMenu(self.screen, self.save_data)
            elif action == 'settings':
                self.state = 'settings'
            elif action == 'quit':
                pygame.quit()
                exit()

        elif self.state == 'hero_select':
            action = self.hero_select.handle_event(event)
            if action == 'back':
                self.state = 'menu'
            elif action and action in self.heroes:
                # Выбран герой
                self.selected_hero = action
                self.save_data['selected_hero'] = action
                SaveSystem.save_game(self.save_data)
                self.state = 'menu'

        elif self.state == 'settings':
            action = self.settings_menu.handle_event(event)
            if action == 'back':
                self.state = 'menu'

        elif self.state == 'battle':
            if self.arena:
                action = self.arena.handle_event(event)
                if action == 'back_to_menu':
                    self.state = 'menu'

    def start_battle(self):
        """Начать битву"""
        # Создаём героя игрока
        hero_class = self.heroes[self.selected_hero]
        player = hero_class(300, GROUND_Y, is_player=True)

        # Создаём случайного врага (включая всех доступных героев)
        import random
        enemy_heroes = ['warrior', 'mage', 'archer']
        enemy_choice = random.choice(enemy_heroes)
        enemy_class = self.heroes[enemy_choice]
        enemy = enemy_class(SCREEN_WIDTH - 300, GROUND_Y, is_player=False)

        self.arena = Arena(self.screen, player, enemy, self.save_data)
        self.state = 'battle'

    def update(self, dt):
        """Обновление текущего состояния"""
        if self.state == 'battle' and self.arena:
            result = self.arena.update()
            if result == 'player_win':
                # Победа игрока
                self.save_data['cups'] += 50
                self.save_data['wins'] += 1
                SaveSystem.save_game(self.save_data)
                self.state = 'menu'
            elif result == 'enemy_win':
                # Поражение
                self.save_data['cups'] = max(0, self.save_data['cups'] - 25)
                self.save_data['losses'] += 1
                SaveSystem.save_game(self.save_data)
                self.state = 'menu'

    def draw(self):
        """Отрисовка текущего состояния"""
        if self.state == 'menu':
            self.menu.draw(self.save_data)
        elif self.state == 'hero_select' and self.hero_select:
            self.hero_select.draw(self.save_data)
        elif self.state == 'settings':
            self.settings_menu.draw()
        elif self.state == 'battle' and self.arena:
            self.arena.draw()