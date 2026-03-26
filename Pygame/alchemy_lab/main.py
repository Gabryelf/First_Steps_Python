# main.py
import pygame
import sys
from config import *
from game import Game


class GameUI:
    """Класс для отрисовки и обработки ввода"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Алхимическая лаборатория")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.game = Game()

        # Для drag-n-drop
        self.dragged_element = None
        self.drag_start_pos = (0, 0)

    def draw_inventory(self):
        """Рисует все элементы инвентаря в сетку"""
        margin = 20
        start_x = margin
        start_y = SCREEN_HEIGHT - ELEMENT_SIZE - margin
        cols = (SCREEN_WIDTH - margin) // (ELEMENT_SIZE + 10)

        for idx, element in enumerate(self.game.alchemist.inventory):
            col = idx % cols
            row = idx // cols
            x = start_x + col * (ELEMENT_SIZE + 10)
            y = start_y - row * (ELEMENT_SIZE + 10)
            element.draw(self.screen, x, y)

        # Текст "Инвентарь"
        inv_text = self.small_font.render("Инвентарь (перетащи для смешивания)", True, DARK_GRAY)
        self.screen.blit(inv_text, (margin, SCREEN_HEIGHT - margin - ELEMENT_SIZE - 10))

    def draw_info(self):
        """Рисует сообщения и подсказки"""
        # Верхняя панель
        pygame.draw.rect(self.screen, GRAY, (0, 0, SCREEN_WIDTH, 50))

        # Сообщение
        msg_surf = self.font.render(self.game.message, True, BLACK)
        self.screen.blit(msg_surf, (10, 15))

        # Кнопка сохранения
        save_btn = pygame.Rect(SCREEN_WIDTH - 100, 10, 90, 30)
        pygame.draw.rect(self.screen, DARK_GRAY, save_btn)
        save_text = self.font.render("Сохранить", True, WHITE)
        self.screen.blit(save_text, (save_btn.x + 10, save_btn.y + 5))

        # Счетчик открытых элементов
        counter_text = self.font.render(f"Открыто: {len(self.game.alchemist.inventory)} элементов", True, BLACK)
        self.screen.blit(counter_text, (SCREEN_WIDTH - 250, 15))

        return save_btn

    def get_element_at_pos(self, pos):
        """Возвращает элемент, на который нажали"""
        for element in self.game.alchemist.inventory:
            if element.rect and element.rect.collidepoint(pos):
                return element
        return None

    def run(self):
        running = True
        while running:
            self.screen.fill(WHITE)

            # Отрисовка
            save_btn = self.draw_info()
            self.draw_inventory()

            # Если что-то тащим, рисуем призрак
            if self.dragged_element:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.dragged_element.draw(self.screen, mouse_x - ELEMENT_SIZE // 2, mouse_y - ELEMENT_SIZE // 2)

            pygame.display.flip()

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if save_btn.collidepoint(event.pos):
                        self.game.save()
                        self.game.message = "Игра сохранена!"
                        self.game.message_timer = 60
                    else:
                        # Начинаем перетаскивание
                        self.dragged_element = self.get_element_at_pos(event.pos)
                        if self.dragged_element:
                            self.drag_start_pos = event.pos

                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.dragged_element:
                        # Пытаемся смешать с элементом под курсором
                        target = self.get_element_at_pos(event.pos)
                        if target and target != self.dragged_element:
                            self.game.try_combine(self.dragged_element, target)
                        self.dragged_element = None

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.game.save()
                        self.game.message = "Игра сохранена (Ctrl+S)!"
                        self.game.message_timer = 60

            self.game.update_message()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    ui = GameUI()
    ui.run()