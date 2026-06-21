import pygame
from typing import List
from models.card import Card
from models.entity import Entity


class Renderer:
    """Отвечает за отрисовку игры"""

    def __init__(self, screen_width=800, screen_height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Карточный Рогалик")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Цвета
        self.colors = {
            'background': (40, 44, 52),
            'text': (255, 255, 255),
            'hero': (86, 156, 214),
            'enemy': (220, 163, 163),
            'card': (62, 68, 81),
            'card_highlight': (97, 175, 239)
        }

    def draw_entity(self, entity: Entity, x: int, y: int, color: tuple):
        """Отрисовка существа"""
        pygame.draw.rect(self.screen, color, (x, y, 200, 100), border_radius=10)
        name_text = self.font.render(entity.name, True, self.colors['text'])
        health_text = self.small_font.render(
            f"HP: {entity.current_health}/{entity.max_health}",
            True, self.colors['text']
        )
        self.screen.blit(name_text, (x + 10, y + 10))
        self.screen.blit(health_text, (x + 10, y + 50))

    def draw_card(self, card: Card, x: int, y: int, width: int, height: int, highlight=False):
        """Отрисовка карты"""
        color = self.colors['card_highlight'] if highlight else self.colors['card']
        pygame.draw.rect(self.screen, color, (x, y, width, height), border_radius=8)

        name_text = self.small_font.render(card.name, True, self.colors['text'])
        cost_text = self.small_font.render(f"Энергия: {card.energy_cost}", True, self.colors['text'])
        desc_text = self.small_font.render(card.description, True, self.colors['text'])

        self.screen.blit(name_text, (x + 10, y + 10))
        self.screen.blit(cost_text, (x + 10, y + 30))
        self.screen.blit(desc_text, (x + 10, y + 50))

    def draw_hand(self, cards: List[Card], selected_index: int = -1):
        """Отрисовка карт в руке"""
        card_width, card_height = 150, 80
        spacing = 10
        total_width = len(cards) * (card_width + spacing) - spacing
        start_x = (800 - total_width) // 2

        for i, card in enumerate(cards):
            highlight = (i == selected_index)
            self.draw_card(card, start_x + i * (card_width + spacing),
                           450, card_width, card_height, highlight)

    def draw_message_log(self, messages: List[str]):
        """Отрисовка лога сообщений"""
        for i, message in enumerate(messages[-5:]):  # Последние 5 сообщений
            text = self.small_font.render(message, True, self.colors['text'])
            self.screen.blit(text, (10, 350 + i * 25))

    def draw_energy(self, current: int, max_energy: int):
        """Отрисовка энергии"""
        energy_text = self.font.render(f"Энергия: {current}/{max_energy}", True, self.colors['text'])
        self.screen.blit(energy_text, (600, 100))

    def clear_screen(self):
        """Очистка экрана"""
        self.screen.fill(self.colors['background'])

    def update_display(self):
        """Обновление экрана"""
        pygame.display.flip()
        self.clock.tick(60)