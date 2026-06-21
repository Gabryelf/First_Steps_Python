import pygame
import sys
from typing import Dict, Any
from datetime import datetime
from models.game_state import GameState
from models.player import Player
from graphics.renderer import Renderer
from graphics.menu import Menu
from models.hero import Hero

from persistence.game_repository import GameRepository
from persistence.file_repository import FileGameRepository


class CardRoguelikeGame:
    """Главный класс игры с меню и сохранениями"""

    def __init__(self):
        pygame.init()  # Инициализируем pygame здесь

        self.game_state = GameState()
        self.renderer = Renderer()
        self.menu = Menu(self.renderer)
        #self.repository = GameRepository()
        self.repository = FileGameRepository()  # вместо GameRepository()

        self.current_screen = "main_menu"
        self.selected_menu_index = 0
        self.selected_creation_field = 0
        self.selected_class = 0
        self.player_name_input = ""
        self.hero_name_input = ""

        self.running = True

        # Для отладки
        print("Игра инициализирована. Текущий экран:", self.current_screen)

    def handle_main_menu_events(self, event):
        """Обработка событий главного меню"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_menu_index = (self.selected_menu_index - 1) % 4
                print("Выбрано:", self.selected_menu_index)
            elif event.key == pygame.K_DOWN:
                self.selected_menu_index = (self.selected_menu_index + 1) % 4
                print("Выбрано:", self.selected_menu_index)
            elif event.key == pygame.K_RETURN:
                if self.selected_menu_index == 0:  # Новая игра
                    self.current_screen = "player_creation"
                    print("Переход к созданию персонажа")
                elif self.selected_menu_index == 1:  # Загрузить игру
                    self.current_screen = "load_game"
                    print("Переход к загрузке игры")
                elif self.selected_menu_index == 2:  # Лидерборд
                    self.current_screen = "leaderboard"
                    print("Переход к таблице лидеров")
                elif self.selected_menu_index == 3:  # Выход
                    self.running = False
                    print("Выход из игры")

    def handle_player_creation_events(self, event):
        """Обработка событий создания игрока"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_creation_field = (self.selected_creation_field - 1) % 3
                print("Выбрано поле:", self.selected_creation_field)
            elif event.key == pygame.K_DOWN:
                self.selected_creation_field = (self.selected_creation_field + 1) % 3
                print("Выбрано поле:", self.selected_creation_field)
            elif event.key == pygame.K_LEFT and self.selected_creation_field == 2:
                self.selected_class = (self.selected_class - 1) % 3
                print("Выбран класс:", self.selected_class)
            elif event.key == pygame.K_RIGHT and self.selected_creation_field == 2:
                self.selected_class = (self.selected_class + 1) % 3
                print("Выбран класс:", self.selected_class)
            elif event.key == pygame.K_RETURN:
                if self.player_name_input.strip() and self.hero_name_input.strip():
                    print(f"Создание игры: игрок='{self.player_name_input}', герой='{self.hero_name_input}'")
                    self.start_new_game()
                else:
                    print("Ошибка: не заполнены все поля!")
            elif event.key == pygame.K_BACKSPACE:
                if self.selected_creation_field == 0:
                    self.player_name_input = self.player_name_input[:-1]
                    print("Имя игрока:", self.player_name_input)
                elif self.selected_creation_field == 1:
                    self.hero_name_input = self.hero_name_input[:-1]
                    print("Имя героя:", self.hero_name_input)
            elif event.key == pygame.K_ESCAPE:
                self.current_screen = "main_menu"
                print("Возврат в главное меню")
            else:
                # Ввод текста
                if event.unicode.isprintable() and len(event.unicode) > 0:
                    if self.selected_creation_field == 0 and len(self.player_name_input) < 20:
                        self.player_name_input += event.unicode
                        print("Имя игрока:", self.player_name_input)
                    elif self.selected_creation_field == 1 and len(self.hero_name_input) < 20:
                        self.hero_name_input += event.unicode
                        print("Имя героя:", self.hero_name_input)

    def handle_game_events(self, event):
        """Обработка событий игрового экрана"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # СОХРАНЕНИЕ ПРИ ВЫХОДЕ В МЕНЮ
                if self.game_state.hero:
                    hero_data = self.game_state.hero.get_save_data()
                    game_state_data = self.game_state.get_save_data()
                    self.repository.save_game(
                        self.game_state.player_name,
                        hero_data,
                        game_state_data
                    )
                    print("Игра сохранена при выходе в меню")

                self.current_screen = "main_menu"
                print("Возврат в главное меню из игры")

            # Выбор карт цифрами 1-5
            elif pygame.K_1 <= event.key <= pygame.K_5:
                card_index = event.key - pygame.K_1
                if (self.game_state.hero and
                        card_index < len(self.game_state.hero.get_hand())):
                    self.selected_card_index = card_index
                    print(f"Выбрана карта {card_index + 1}")

            # Использование выбранной карты
            elif event.key == pygame.K_SPACE and hasattr(self, 'selected_card_index') and self.selected_card_index >= 0:
                if self.game_state.is_player_turn:
                    result = self.game_state.player_play_card(self.selected_card_index)
                    print("Результат использования карты:", result)
                    self.selected_card_index = -1

                    # АВТОСОХРАНЕНИЕ ПОСЛЕ ХОДА
                    if self.game_state.hero and not self.game_state.game_over:
                        hero_data = self.game_state.hero.get_save_data()
                        game_state_data = self.game_state.get_save_data()
                        self.repository.save_game(
                            self.game_state.player_name,
                            hero_data,
                            game_state_data
                        )
                        print("Автосохранение выполнено")

            # Завершение хода
            elif event.key == pygame.K_w:
                self.game_state.end_player_turn()
                print("Ход завершен")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Простая обработка клика по картам
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (self.game_state.hero and
                    450 <= mouse_y <= 530):  # Область карт
                cards = self.game_state.hero.get_hand()
                card_width = 150
                spacing = 10
                total_width = len(cards) * (card_width + spacing) - spacing
                start_x = (800 - total_width) // 2

                for i in range(len(cards)):
                    card_x = start_x + i * (card_width + spacing)
                    if card_x <= mouse_x <= card_x + card_width:
                        self.selected_card_index = i
                        print(f"Выбрана карта {i + 1} кликом")
                        break

    def start_new_game(self):
        """Начало новой игры"""
        try:
            print("Начинаем создание новой игры...")

            # Сохраняем имя текущего игрока
            self.current_player_name = self.player_name_input

            # Создаем игрока если не существует
            if not self.repository.get_player(self.current_player_name):
                self.repository.create_player(self.current_player_name)

            classes = ["Воин", "Маг", "Лучник"]
            selected_class = classes[self.selected_class]

            print(f"Создание героя: {self.hero_name_input}, класс: {selected_class}")

            # Инициализируем игру
            self.game_state.initialize_new_game(
                self.current_player_name,
                self.hero_name_input,
                selected_class
            )

            # СОХРАНЯЕМ ИГРУ ПОСЛЕ СОЗДАНИЯ
            if self.game_state.hero:
                hero_data = self.game_state.hero.get_save_data()
                game_state_data = self.game_state.get_save_data()
                self.repository.save_game(
                    self.current_player_name,
                    hero_data,
                    game_state_data
                )
                print("Новая игра сохранена!")

            # Инициализируем выбор карты
            self.selected_card_index = -1

            # Переключаем экран
            self.current_screen = "game"
            print("Успешно перешли к игровому экрану")

        except Exception as e:
            print(f"Ошибка при создании игры: {e}")
            import traceback
            traceback.print_exc()

    def draw_game_screen(self):
        """Отрисовка игрового экрана"""
        # Отрисовка героя и врага
        if self.game_state.hero:
            self.renderer.draw_entity(self.game_state.hero, 50, 100, self.renderer.colors['hero'])
            self.renderer.draw_energy(
                self.game_state.hero.energy,
                self.game_state.hero.max_energy
            )

            # Отрисовка уровня и опыта
            level_text = self.renderer.small_font.render(
                f"Уровень: {self.game_state.hero.level} Опыт: {self.game_state.hero.experience}",
                True, self.renderer.colors['text']
            )
            gold_text = self.renderer.small_font.render(
                f"Золото: {self.game_state.hero.gold}",
                True, self.renderer.colors['text']
            )
            self.renderer.screen.blit(level_text, (50, 220))
            self.renderer.screen.blit(gold_text, (50, 250))

        if self.game_state.current_enemy:
            self.renderer.draw_entity(
                self.game_state.current_enemy,
                550, 100,
                self.renderer.colors['enemy']
            )

            # Отрисовка этажа
            floor_text = self.renderer.small_font.render(
                f"Этаж: {self.game_state.current_floor}",
                True, self.renderer.colors['text']
            )
            self.renderer.screen.blit(floor_text, (550, 220))

        # Отрисовка карт в руке
        if self.game_state.hero:
            self.renderer.draw_hand(
                self.game_state.hero.get_hand(),
                self.selected_card_index if hasattr(self, 'selected_card_index') else -1
            )

        # Отрисовка лога сообщений
        self.renderer.draw_message_log(self.game_state.message_log)

        # Отрисовка подсказок
        hints = [
            "1-5: выбрать карту",
            "SPACE: использовать",
            "W: закончить ход",
            "ESC: в меню"
        ]
        for i, hint in enumerate(hints):
            hint_text = self.renderer.small_font.render(hint, True, self.renderer.colors['text'])
            self.renderer.screen.blit(hint_text, (10, 500 + i * 25))

        # Отрисовка текущего хода
        turn_text = self.renderer.small_font.render(
            "Ваш ход" if self.game_state.is_player_turn else "Ход врага",
            True, self.renderer.colors['text']
        )
        self.renderer.screen.blit(turn_text, (350, 50))

        # Отрисовка информации о герое
        if self.game_state.hero:
            hero_info = self.renderer.small_font.render(
                f"{self.game_state.hero.name} ({self.game_state.hero.hero_class})",
                True, self.renderer.colors['text']
            )
            self.renderer.screen.blit(hero_info, (50, 70))

    # Добавьте эти методы в класс CardRoguelikeGame:

    def handle_load_menu_events(self, event):
        """Обработка событий меню загрузки"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_screen = "main_menu"
                print("Возврат в главное меню")

            elif event.key == pygame.K_UP and self.load_menu_saves:
                self.load_menu_selected_index = (self.load_menu_selected_index - 1) % len(self.load_menu_saves)
                print(f"Выбрано сохранение: {self.load_menu_selected_index}")

            elif event.key == pygame.K_DOWN and self.load_menu_saves:
                self.load_menu_selected_index = (self.load_menu_selected_index + 1) % len(self.load_menu_saves)
                print(f"Выбрано сохранение: {self.load_menu_selected_index}")

            elif event.key == pygame.K_RETURN and self.load_menu_saves:
                if self.load_menu_saves and 0 <= self.load_menu_selected_index < len(self.load_menu_saves):
                    self.load_selected_game()

            elif event.key == pygame.K_DELETE and self.load_menu_saves:
                # Опционально: удаление сохранения
                if self.load_menu_saves and 0 <= self.load_menu_selected_index < len(self.load_menu_saves):
                    self.delete_selected_save()

    def load_selected_game(self):
        """Загрузка выбранной игры"""
        try:
            selected_save = self.load_menu_saves[self.load_menu_selected_index]
            player_name = self.current_player_name  # Нужно где-то хранить текущего игрока
            hero_name = selected_save['hero_name']

            print(f"Загрузка игры: {player_name} - {hero_name}")

            # Загружаем данные сохранения
            save_data = self.repository.load_game(player_name, hero_name)

            if not save_data:
                print("Ошибка: сохранение не найдено")
                return

            # Восстанавливаем состояние игры
            self.load_game_state(save_data)

            # Переходим к игровому экрану
            self.current_screen = "game"
            self.selected_card_index = -1

            print(f"Игра успешно загружена: {hero_name} уровень {self.game_state.hero.level}")

        except Exception as e:
            print(f"Ошибка при загрузке игры: {e}")
            import traceback
            traceback.print_exc()

    def load_game_state(self, save_data: Dict[str, Any]):
        """Восстановление состояния игры из данных сохранения"""
        try:
            # Создаем нового героя на основе сохраненных данных
            from models.hero import Hero

            hero_data = save_data['hero_data']
            game_state_data = save_data['game_state']

            # Создаем героя
            self.game_state.hero = Hero(hero_data['name'], hero_data['hero_class'])

            # Восстанавливаем параметры героя
            self.game_state.hero.level = hero_data.get('level', 1)
            self.game_state.hero.experience = hero_data.get('experience', 0)
            self.game_state.hero.gold = hero_data.get('gold', 0)
            self.game_state.hero._max_health = hero_data.get('max_health', 100)
            self.game_state.hero._current_health = hero_data.get('current_health', 100)
            self.game_state.hero.permanent_upgrades = hero_data.get('permanent_upgrades', {})

            # Восстанавливаем состояние игры
            self.game_state.current_floor = game_state_data.get('current_floor', 1)
            self.game_state.enemies_defeated = game_state_data.get('enemies_defeated', 0)
            self.game_state.is_player_turn = game_state_data.get('is_player_turn', True)
            self.game_state.game_over = game_state_data.get('game_over', False)
            self.game_state.player_name = save_data['player_name']

            # Генерируем врага для текущего этажа
            self.game_state._generate_enemy()

            # Восстанавливаем руку героя
            self.game_state.hero.start_turn()

            # Добавляем сообщение в лог
            self.game_state.message_log = [
                f"Игра загружена: {self.game_state.hero.name} уровень {self.game_state.hero.level}"]

            print("Состояние игры успешно восстановлено")

        except Exception as e:
            print(f"Ошибка при восстановлении состояния игры: {e}")
            import traceback
            traceback.print_exc()

    def delete_selected_save(self):
        """Удаление выбранного сохранения"""
        # Пока оставим пустым - можно реализовать позже
        print("Функция удаления сохранения пока не реализована")

    def run(self):
        """Главный игровой цикл"""
        print("Запуск игрового цикла...")

        # Инициализируем переменные для меню загрузки
        self.load_menu_saves = []
        self.load_menu_selected_index = 0
        self.current_player_name = ""  # Будет устанавливаться при создании/загрузке

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    print("Выход из игры по закрытию окна")

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.current_screen == "game":
                            # СОХРАНЕНИЕ ПРИ ВЫХОДЕ В МЕНЮ
                            if self.game_state.hero:
                                hero_data = self.game_state.hero.get_save_data()
                                game_state_data = self.game_state.get_save_data()
                                self.repository.save_game(
                                    self.game_state.player_name,
                                    hero_data,
                                    game_state_data
                                )
                                print("Игра сохранена при выходе в меню")

                            self.current_screen = "main_menu"
                            print("Возврат в главное меню из игры")
                        else:
                            self.running = False
                            print("Выход из игры по ESC")

                # Обработка в зависимости от текущего экрана
                if self.current_screen == "main_menu":
                    self.handle_main_menu_events(event)
                elif self.current_screen == "player_creation":
                    self.handle_player_creation_events(event)
                elif self.current_screen == "load_game":
                    self.handle_load_menu_events(event)
                elif self.current_screen == "game":
                    self.handle_game_events(event)
                elif self.current_screen == "leaderboard":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.current_screen = "main_menu"
                        print("Возврат из лидерборда в главное меню")

            # Отрисовка
            self.renderer.clear_screen()

            if self.current_screen == "main_menu":
                self.menu.draw_main_menu(self.selected_menu_index)

                # Подсказка
                hint = self.renderer.small_font.render(
                    "↑↓: выбор, ENTER: подтвердить, ESC: выход",
                    True, self.renderer.colors['text']
                )
                self.renderer.screen.blit(hint, (400 - hint.get_width() // 2, 500))

            elif self.current_screen == "player_creation":
                self.menu.draw_player_creation(
                    self.player_name_input,
                    self.hero_name_input,
                    self.selected_class,
                    self.selected_creation_field
                )

                # Подсказки
                hints = [
                    "↑↓: выбор поля, ←→: выбор класса",
                    "BACKSPACE: удалить, ENTER: начать игру",
                    "ESC: назад"
                ]
                for i, hint in enumerate(hints):
                    hint_text = self.renderer.small_font.render(hint, True, self.renderer.colors['text'])
                    self.renderer.screen.blit(hint_text, (400 - hint_text.get_width() // 2, 450 + i * 25))

                # Предупреждение о незаполненных полях
                if not self.player_name_input.strip() or not self.hero_name_input.strip():
                    warning = self.renderer.small_font.render(
                        "Заполните все поля!",
                        True, (255, 100, 100)
                    )
                    self.renderer.screen.blit(warning, (400 - warning.get_width() // 2, 550))

            elif self.current_screen == "load_game":
                # Загружаем список сохранений при входе в меню
                if not self.load_menu_saves and self.player_name_input:  # Используем имя из создания персонажа
                    self.current_player_name = self.player_name_input
                    self.load_menu_saves = self.repository.get_player_saves(self.current_player_name)
                    print(f"Загружено сохранений: {len(self.load_menu_saves)}")

                self.menu.draw_load_menu(self.load_menu_saves, self.load_menu_selected_index)

                # Подсказки
                if self.load_menu_saves:
                    hints = [
                        "↑↓: выбор сохранения",
                        "ENTER: загрузить игру",
                        "ESC: назад"
                    ]
                else:
                    hints = ["ESC: назад"]

                for i, hint in enumerate(hints):
                    hint_text = self.renderer.small_font.render(hint, True, self.renderer.colors['text'])
                    self.renderer.screen.blit(hint_text, (400 - hint_text.get_width() // 2, 500 + i * 25))

            elif self.current_screen == "leaderboard":
                try:
                    leaderboard_data = self.repository.get_leaderboard()
                    self.menu.draw_leaderboard(leaderboard_data)

                    # Подсказка
                    hint = self.renderer.small_font.render(
                        "ESC: назад",
                        True, self.renderer.colors['text']
                    )
                    self.renderer.screen.blit(hint, (400 - hint.get_width() // 2, 500))

                except Exception as e:
                    print(f"Ошибка при загрузке лидерборда: {e}")
                    error_text = self.renderer.small_font.render(
                        "Ошибка загрузки лидерборда",
                        True, (255, 100, 100)
                    )
                    self.renderer.screen.blit(error_text, (400 - error_text.get_width() // 2, 300))

            elif self.current_screen == "game":
                self.draw_game_screen()

            self.renderer.update_display()

        pygame.quit()
        sys.exit()





if __name__ == "__main__":
    try:
        game = CardRoguelikeGame()
        game.run()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        import traceback

        traceback.print_exc()
        input("Нажмите Enter для выхода...")