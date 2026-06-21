from datetime import datetime

import pygame
from typing import List, Dict, Any, Callable


class Menu:
    """Класс для отрисовки меню"""

    def __init__(self, renderer):
        self.renderer = renderer
        self.colors = renderer.colors

    def draw_main_menu(self, selected_index: int):
        """Отрисовка главного меню"""
        options = ["Новая игра", "Загрузить игру", "Таблица лидеров", "Выход"]

        for i, option in enumerate(options):
            color = self.colors['card_highlight'] if i == selected_index else self.colors['text']
            text = self.renderer.font.render(option, True, color)
            self.renderer.screen.blit(text, (400 - text.get_width() // 2, 200 + i * 60))

    def draw_player_creation(self, player_name: str, hero_name: str, selected_class: int, selected_field: int):
        """Отрисовка меню создания игрока"""
        classes = ["Воин", "Маг", "Лучник"]

        # Поля ввода
        fields = [
            f"Игрок: {player_name}",
            f"Имя героя: {hero_name}",
            f"Класс: {classes[selected_class]}"
        ]

        for i, field in enumerate(fields):
            color = self.colors['card_highlight'] if i == selected_field else self.colors['text']
            text = self.renderer.font.render(field, True, color)
            self.renderer.screen.blit(text, (400 - text.get_width() // 2, 200 + i * 60))

        # Описание классов
        class_descriptions = {
            "Воин": "Высокое здоровье, сильные атаки",
            "Маг": "Мощные заклинания, дополнительная энергия",
            "Лучник": "Высокий урон, разнообразные атаки"
        }

        desc_text = self.renderer.small_font.render(
            class_descriptions[classes[selected_class]],
            True, self.colors['text']
        )
        self.renderer.screen.blit(desc_text, (400 - desc_text.get_width() // 2, 400))

    def draw_leaderboard(self, leaderboard_data: List[Dict[str, Any]]):
        """Отрисовка таблицы лидеров"""
        title = self.renderer.font.render("ТАБЛИЦА ЛИДЕРОВ", True, self.colors['text'])
        self.renderer.screen.blit(title, (400 - title.get_width() // 2, 50))

        headers = ["Игрок", "Герой", "Уровень", "Очки"]
        for i, header in enumerate(headers):
            text = self.renderer.small_font.render(header, True, self.colors['card_highlight'])
            self.renderer.screen.blit(text, (100 + i * 150, 120))

        for i, entry in enumerate(leaderboard_data):
            y_pos = 150 + i * 30
            texts = [
                entry.get('player_name', ''),
                entry.get('hero_name', ''),
                str(entry.get('level', 0)),
                str(entry.get('score', 0))
            ]

            for j, text in enumerate(texts):
                rendered = self.renderer.small_font.render(text, True, self.colors['text'])
                self.renderer.screen.blit(rendered, (100 + j * 150, y_pos))

    def draw_load_menu(self, saves_data: List[Dict[str, Any]], selected_index: int):
        """Отрисовка меню загрузки игры"""
        title = self.renderer.font.render("ЗАГРУЗКА ИГРЫ", True, self.colors['text'])
        self.renderer.screen.blit(title, (400 - title.get_width() // 2, 50))

        if not saves_data:
            # Если сохранений нет
            no_saves_text = self.renderer.font.render("Нет сохраненных игр", True, self.colors['text'])
            self.renderer.screen.blit(no_saves_text, (400 - no_saves_text.get_width() // 2, 200))

            hint_text = self.renderer.small_font.render("Создайте новую игру в главном меню", True, self.colors['text'])
            self.renderer.screen.blit(hint_text, (400 - hint_text.get_width() // 2, 250))
        else:
            # Отображаем список сохранений
            headers = ["Герой", "Уровень", "Последнее сохранение"]
            for i, header in enumerate(headers):
                text = self.renderer.small_font.render(header, True, self.colors['card_highlight'])
                self.renderer.screen.blit(text, (100 + i * 200, 120))

            for i, save in enumerate(saves_data):
                y_pos = 150 + i * 40
                color = self.colors['card_highlight'] if i == selected_index else self.colors['text']

                # Имя героя
                hero_text = self.renderer.small_font.render(save.get('hero_name', 'Неизвестно'), True, color)
                self.renderer.screen.blit(hero_text, (100, y_pos))

                # Уровень
                level_text = self.renderer.small_font.render(f"Ур. {save.get('level', 1)}", True, color)
                self.renderer.screen.blit(level_text, (300, y_pos))

                # Дата сохранения
                last_saved = save.get('last_saved')
                if last_saved:
                    if isinstance(last_saved, datetime):
                        date_str = last_saved.strftime("%d.%m.%Y %H:%M")
                    else:
                        date_str = str(last_saved)[:16]  # Берем первую часть строки
                else:
                    date_str = "Неизвестно"

                date_text = self.renderer.small_font.render(date_str, True, color)
                self.renderer.screen.blit(date_text, (500, y_pos))