import pygame
import sys
from models.game_state import GameState
from graphics.renderer import Renderer
from persistence.game_repository import GameRepository


class CardRoguelikeGame:
    """Главный класс игры"""

    def __init__(self):
        self.game_state = GameState()
        self.renderer = Renderer()
        self.repository = GameRepository()
        self.selected_card_index = -1
        self.running = True

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # Выбор карт цифрами 1-5
                elif pygame.K_1 <= event.key <= pygame.K_5:
                    card_index = event.key - pygame.K_1
                    if card_index < len(self.game_state.hero.get_hand()):
                        self.selected_card_index = card_index

                # Использование выбранной карты
                elif event.key == pygame.K_SPACE and self.selected_card_index >= 0:
                    if self.game_state.is_player_turn:
                        self.game_state.player_play_card(self.selected_card_index)
                        self.selected_card_index = -1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Простая обработка клика по картам
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 450 <= mouse_y <= 530:  # Область карт
                    card_width = 150
                    spacing = 10
                    start_x = (800 - len(self.game_state.hero.get_hand()) * (card_width + spacing)) // 2

                    for i in range(len(self.game_state.hero.get_hand())):
                        card_x = start_x + i * (card_width + spacing)
                        if card_x <= mouse_x <= card_x + card_width:
                            self.selected_card_index = i
                            break

    def run(self):
        """Главный игровой цикл"""
        # Инициализация новой игры (позже добавим меню)
        self.game_state.initialize_game("Студент-Герой")

        while self.running:
            self.handle_events()

            # Отрисовка
            self.renderer.clear_screen()

            # Отрисовка героя и врага
            if self.game_state.hero:
                self.renderer.draw_entity(self.game_state.hero, 50, 100, self.renderer.colors['hero'])
                self.renderer.draw_energy(
                    self.game_state.hero.energy,
                    self.game_state.hero.max_energy
                )

            if self.game_state.current_enemy:
                self.renderer.draw_entity(
                    self.game_state.current_enemy,
                    550, 100,
                    self.renderer.colors['enemy']
                )

            # Отрисовка карт в руке
            if self.game_state.hero:
                self.renderer.draw_hand(
                    self.game_state.hero.get_hand(),
                    self.selected_card_index
                )

            # Отрисовка лога сообщений
            self.renderer.draw_message_log(self.game_state.message_log)

            # Отрисовка подсказок
            hint_text = self.renderer.small_font.render(
                "1-5: выбрать карту, SPACE: использовать, ESC: выход",
                True, self.renderer.colors['text']
            )
            self.renderer.screen.blit(hint_text, (10, 550))

            self.renderer.update_display()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = CardRoguelikeGame()
    game.run()
