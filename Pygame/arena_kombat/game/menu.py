# game/menu.py - система меню

import pygame

from arena_kombat.config.settings import *


class Button:
    """Класс кнопки для меню"""

    def __init__(self, x, y, width, height, text, color=WHITE, hover_color=YELLOW):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.Font(None, 36)

    def handle_event(self, event):
        """Обработка событий кнопки"""
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.color

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, screen):
        """Отрисовка кнопки"""
        pygame.draw.rect(screen, self.current_color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.current_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class MainMenu:
    """Главное меню"""

    def __init__(self, screen):
        self.screen = screen
        self.buttons = []

        # Создаём кнопки
        button_width = 200
        button_height = 50
        start_x = SCREEN_WIDTH // 2 - button_width // 2

        self.start_button = Button(start_x, 300, button_width, button_height, "Начать бой")
        self.hero_button = Button(start_x, 370, button_width, button_height, "Выбор героя")
        self.settings_button = Button(start_x, 440, button_width, button_height, "Настройки")
        self.quit_button = Button(start_x, 510, button_width, button_height, "Выход")

    def handle_event(self, event):
        """Обработка событий меню"""
        if self.start_button.handle_event(event):
            return 'start'
        if self.hero_button.handle_event(event):
            return 'hero_select'
        if self.settings_button.handle_event(event):
            return 'settings'
        if self.quit_button.handle_event(event):
            return 'quit'
        return None

    def draw(self, save_data):
        """Отрисовка главного меню"""
        self.screen.fill(DARK_GRAY)

        # Заголовок
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("BATTLE ARENA", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        # Количество кубков
        cups_font = pygame.font.Font(None, 48)
        cups_text = cups_font.render(f"🏆 {save_data['cups']}", True, YELLOW)
        self.screen.blit(cups_text, (20, 20))

        # Выбранный герой
        hero_names = {
            'warrior': 'Воин',
            'mage': 'Маг',
            'archer': 'Лучник'
        }
        hero_name = hero_names.get(save_data['selected_hero'], 'Воин')
        hero_text = cups_font.render(f"Герой: {hero_name}", True, WHITE)
        self.screen.blit(hero_text, (20, 80))

        # Рисуем кнопки
        self.start_button.draw(self.screen)
        self.hero_button.draw(self.screen)
        self.settings_button.draw(self.screen)
        self.quit_button.draw(self.screen)


class HeroSelectMenu:
    """Меню выбора героя"""

    def __init__(self, screen, save_data):
        self.screen = screen
        self.save_data = save_data
        self.selected_index = 0

        # Список доступных героев
        self.heroes = [
            {'id': 'warrior', 'name': 'Воин', 'cost': 0, 'hp': 120, 'attack': 20},
            {'id': 'mage', 'name': 'Маг', 'cost': 100, 'hp': 80, 'attack': 30},
            {'id': 'archer', 'name': 'Лучник', 'cost': 100, 'hp': 90, 'attack': 25}
        ]

    def handle_event(self, event):
        """Обработка событий"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.heroes)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.heroes)
            elif event.key == pygame.K_RETURN:
                hero = self.heroes[self.selected_index]
                # Проверяем, открыт ли герой
                if hero['id'] in self.save_data['unlocked_heroes']:
                    return hero['id']
                elif self.save_data['cups'] >= hero['cost']:
                    # Покупаем героя
                    self.save_data['cups'] -= hero['cost']
                    self.save_data['unlocked_heroes'].append(hero['id'])
                    from save_system import SaveSystem
                    SaveSystem.save_game(self.save_data)
                    return hero['id']
            elif event.key == pygame.K_ESCAPE:
                return 'back'
        return None

    def draw(self, save_data):
        """Отрисовка меню выбора героя"""
        self.screen.fill(DARK_GRAY)

        # Заголовок
        font = pygame.font.Font(None, 48)
        title = font.render("ВЫБОР ГЕРОЯ", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # Кубки
        cups_text = font.render(f"🏆 {save_data['cups']}", True, YELLOW)
        self.screen.blit(cups_text, (20, 20))

        # Список героев
        y = 150
        for i, hero in enumerate(self.heroes):
            color = YELLOW if i == self.selected_index else WHITE

            # Название героя
            name_text = font.render(hero['name'], True, color)
            self.screen.blit(name_text, (200, y))

            # Характеристики
            stats_font = pygame.font.Font(None, 24)
            stats = f"HP: {hero['hp']} | Атака: {hero['attack']}"
            stats_text = stats_font.render(stats, True, WHITE)
            self.screen.blit(stats_text, (200, y + 35))

            # Статус (открыт/закрыт)
            if hero['id'] in save_data['unlocked_heroes']:
                status = "ДОСТУПЕН"
                status_color = GREEN
            else:
                status = f"Нужно: {hero['cost']} 🏆"
                status_color = RED

            status_text = stats_font.render(status, True, status_color)
            self.screen.blit(status_text, (SCREEN_WIDTH - 200, y + 20))

            y += 100

        # Подсказка
        hint_font = pygame.font.Font(None, 24)
        hint = hint_font.render("↑/↓ - выбор | ENTER - выбрать/купить | ESC - назад", True, GRAY)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)


class SettingsMenu:
    """Меню настроек"""

    def __init__(self, screen):
        self.screen = screen
        self.sound_volume = 0.7
        self.music_volume = 0.5

    def handle_event(self, event):
        """Обработка событий"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'back'
        return None

    def draw(self):
        """Отрисовка настроек"""
        self.screen.fill(DARK_GRAY)

        font = pygame.font.Font(None, 48)
        title = font.render("НАСТРОЙКИ", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # Текст-заглушка
        info_font = pygame.font.Font(None, 32)
        info = info_font.render("Настройки в разработке", True, WHITE)
        info_rect = info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(info, info_rect)

        hint_font = pygame.font.Font(None, 24)
        hint = hint_font.render("ESC - назад", True, GRAY)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)