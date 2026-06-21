import pygame
from typing import List
from models.card import Card
from models.entity import Entity


class Renderer:
    """Отвечает за отрисовку игры"""

    def __init__(self, screen_width=1000, screen_height=620):  # Увеличили размер экрана
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Карточный Рогалик")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)

        # Цвета
        self.colors = {
            'background': (30, 33, 40),
            'panel': (44, 49, 60),
            'text': (220, 220, 220),
            'text_highlight': (255, 255, 255),
            'hero': (86, 156, 214),
            'enemy': (220, 100, 100),
            'card': (62, 68, 81),
            'card_highlight': (97, 175, 239),
            'energy': (255, 204, 0),
            'health': (224, 58, 69),
            'experience': (106, 176, 76),
            'gold': (255, 215, 0)
        }

    def draw_panel(self, x: int, y: int, width: int, height: int, title: str = ""):
        """Отрисовка панели с закругленными углами"""
        # Основная панель
        pygame.draw.rect(self.screen, self.colors['panel'], (x, y, width, height), border_radius=12)
        pygame.draw.rect(self.screen, (60, 65, 78), (x, y, width, height), 2, border_radius=12)

        # Заголовок если есть
        if title:
            title_text = self.small_font.render(title, True, self.colors['text_highlight'])
            title_bg = pygame.Rect(x + 10, y - 8, title_text.get_width() + 10, 20)
            pygame.draw.rect(self.screen, self.colors['panel'], title_bg, border_radius=8)
            pygame.draw.rect(self.screen, (60, 65, 78), title_bg, 1, border_radius=8)
            self.screen.blit(title_text, (x + 15, y - 6))

    def draw_health_bar(self, x: int, y: int, width: int, current: int, max_val: int, label: str = ""):
        """Отрисовка полоски здоровья"""
        # Фон полоски
        pygame.draw.rect(self.screen, (60, 60, 70), (x, y, width, 20), border_radius=10)

        # Заполнение здоровья
        if max_val > 0:
            health_width = int((current / max_val) * (width - 4))
            pygame.draw.rect(self.screen, self.colors['health'], (x + 2, y + 2, health_width, 16), border_radius=8)

        # Текст
        if label:
            health_text = self.small_font.render(f"{label}: {current}/{max_val}", True, self.colors['text'])
            self.screen.blit(health_text, (x + width + 10, y))

    def draw_energy_bar(self, x: int, y: int, current: int, max_val: int):
        """Отрисовка энергии в виде шариков"""
        energy_text = self.small_font.render("Энергия:", True, self.colors['text'])
        self.screen.blit(energy_text, (x, y))

        for i in range(max_val):
            color = self.colors['energy'] if i < current else (80, 80, 90)
            pygame.draw.circle(self.screen, color, (x + 90 + i * 25, y + 10), 8)

    def draw_resource_counter(self, x: int, y: int, value: int, icon: str, color: tuple):
        """Отрисовка счетчика ресурсов (золото, опыт)"""
        text = self.small_font.render(f"{icon} {value}", True, color)
        self.screen.blit(text, (x, y))

    def draw_entity(self, entity: Entity, x: int, y: int, color: tuple, is_hero: bool = False):
        """Отрисовка существа с улучшенным дизайном"""
        # Панель существа
        self.draw_panel(x, y, 300, 180, entity.name)

        # Уровень и класс (для героя)
        if is_hero and hasattr(entity, 'level'):
            level_text = self.small_font.render(f"Уровень {entity.level}", True, self.colors['text_highlight'])
            self.screen.blit(level_text, (x + 15, y + 25))

        # Полоска здоровья
        self.draw_health_bar(x + 15, y + 55, 200, entity.current_health, entity.max_health)

        # Энергия (для героя)
        if is_hero and hasattr(entity, 'energy'):
            self.draw_energy_bar(x + 15, y + 85, entity.energy, entity.max_energy)

        # Статус (жив/мертв)
        status_color = (106, 176, 76) if entity.is_alive else (200, 60, 60)
        status_text = "ЖИВ" if entity.is_alive else "ПОВЕРЖЕН"
        status_surface = self.small_font.render(status_text, True, status_color)
        self.screen.blit(status_surface, (x + 230, y + 25))

    def draw_card(self, card: Card, x: int, y: int, width: int, height: int, highlight=False):
        """Отрисовка карты с улучшенным дизайном"""
        # Основная карта
        card_color = self.colors['card_highlight'] if highlight else self.colors['card']
        pygame.draw.rect(self.screen, card_color, (x, y, width, height), border_radius=10)
        pygame.draw.rect(self.screen, (80, 85, 100), (x, y, width, height), 2, border_radius=10)

        # Заголовок карты
        name_text = self.font.render(card.name, True, self.colors['text_highlight'])
        self.screen.blit(name_text, (x + 10, y + 10))

        # Стоимость энергии
        energy_bg = pygame.Rect(x + width - 35, y + 8, 30, 30)
        pygame.draw.rect(self.screen, self.colors['energy'], energy_bg, border_radius=8)
        cost_text = self.small_font.render(str(card.energy_cost), True, (0, 0, 0))
        self.screen.blit(cost_text, (x + width - 25, y + 13))

        # Описание
        desc_text = self.small_font.render(card.description, True, self.colors['text'])
        self.screen.blit(desc_text, (x + 10, y + 45))

    def draw_hand(self, cards: List[Card], selected_index: int = -1):
        """Отрисовка карт в руке"""
        if not cards:
            return

        card_width, card_height = 180, 100
        spacing = 15
        total_width = len(cards) * (card_width + spacing) - spacing
        start_x = (1000 - total_width) // 2

        for i, card in enumerate(cards):
            highlight = (i == selected_index)
            self.draw_card(card, start_x + i * (card_width + spacing),
                           280, card_width, card_height, highlight)

    def draw_message_log(self, messages: List[str]):
        """Отрисовка лога сообщений в отдельной панели"""
        self.draw_panel(20, 400, 400, 130, "СОБЫТИЯ")

        # Берем только последние 6 сообщений (чтобы помещались)
        display_messages = messages[-6:]

        for i, message in enumerate(display_messages):
            # Обрезаем сообщение если слишком длинное
            if len(message) > 45:  # Примерная максимальная длина
                message = message[:42] + "..."

            text = self.small_font.render(message, True, self.colors['text'])
            self.screen.blit(text, (35, 425 + i * 20))

    def draw_game_info(self, hero):
        """Отрисовка информации об игре (этаж, прогресс)"""
        self.draw_panel(440, 400, 540, 130, "ИНФОРМАЦИЯ")

        if hero:
            # Этаж
            floor_text = self.small_font.render(f"Текущий этаж: {getattr(hero, '_floor', 1)}", True,
                                                self.colors['text'])
            self.screen.blit(floor_text, (455, 425))

            # Опыт до следующего уровня
            if hasattr(hero, 'experience') and hasattr(hero, 'level'):
                exp_needed = hero._get_required_experience() if hasattr(hero, '_get_required_experience') else 100
                exp_text = self.small_font.render(f"Опыт: {hero.experience}/{exp_needed}", True,
                                                  self.colors['experience'])
                self.screen.blit(exp_text, (455, 450))

            # Золото
            if hasattr(hero, 'gold'):
                gold_text = self.small_font.render(f"Золото: {hero.gold}", True, self.colors['gold'])
                self.screen.blit(gold_text, (455, 475))

            # Побеждено врагов
            enemies_text = self.small_font.render(f"Побеждено врагов: {getattr(hero, '_enemies_defeated', 0)}", True,
                                                  self.colors['text'])
            self.screen.blit(enemies_text, (455, 500))

    def draw_toolbar(self, hero, current_turn: bool):
        """Отрисовка тулбара с основной информацией"""
        self.draw_panel(20, 20, 960, 60, "")

        if hero:
            # Имя и класс героя
            name_text = self.font.render(f"{hero.name} - {getattr(hero, 'hero_class', 'Авантюрист')}", True,
                                         self.colors['text_highlight'])
            self.screen.blit(name_text, (30, 35))

            # Здоровье в тулбаре
            health_text = self.small_font.render(f"❤ {hero.current_health}/{hero.max_health}", True,
                                                 self.colors['health'])
            self.screen.blit(health_text, (250, 35))

            # Энергия в тулбаре
            energy_text = self.small_font.render(f"⚡ {hero.energy}/{hero.max_energy}", True, self.colors['energy'])
            self.screen.blit(energy_text, (350, 35))

            # Уровень
            level_text = self.small_font.render(f"⭐ Ур. {hero.level}", True, self.colors['experience'])
            self.screen.blit(level_text, (430, 35))

            # Золото
            gold_text = self.small_font.render(f"💰 {hero.gold}", True, self.colors['gold'])
            self.screen.blit(gold_text, (510, 35))

        # Индикатор хода
        turn_color = (106, 176, 76) if current_turn else (200, 60, 60)
        turn_text = "ВАШ ХОД" if current_turn else "ХОД ПРОТИВНИКА"
        turn_surface = self.small_font.render(turn_text, True, turn_color)
        self.screen.blit(turn_surface, (850, 35))

    def clear_screen(self):
        """Очистка экрана"""
        self.screen.fill(self.colors['background'])

    def update_display(self):
        """Обновление экрана"""
        pygame.display.flip()
        self.clock.tick(60)

    def draw_inventory(self, hero, selected_index: int = -1, is_merchant: bool = False):
        """Отрисовка инвентаря или магазина торговца"""
        if is_merchant:
            title = "МАГАЗИН ТОРГОВЦА"
            items = hero.merchant.get_items_for_sale() if hasattr(hero, 'merchant') else []
        else:
            title = "ИНВЕНТАРЬ"
            items = hero.inventory if hero else []

        self.draw_panel(440, 400, 540, 250, title)

        if not items:
            no_items_text = self.small_font.render("Пусто", True, self.colors['text'])
            self.screen.blit(no_items_text, (455, 425))
            return

        # Отображаем до 8 предметов
        for i, item in enumerate(items[:8]):
            y_pos = 425 + i * 28
            color = self.colors['card_highlight'] if i == selected_index else self.colors['text']

            # Название предмета
            name_color = self.colors['gold'] if item.item_type == "weapon" else \
                self.colors['health'] if item.item_type == "potion" else \
                    self.colors['energy'] if item.item_type == "armor" else \
                        self.colors['text_highlight']

            name_text = self.small_font.render(item.name, True, name_color)
            self.screen.blit(name_text, (455, y_pos))

            # Стоимость или описание
            if is_merchant:
                price_text = self.small_font.render(f"{item.value} золота", True, self.colors['gold'])
                self.screen.blit(price_text, (650, y_pos))
            else:
                desc_text = self.small_font.render(item.description, True, self.colors['text'])
                self.screen.blit(desc_text, (650, y_pos))

                # Маркер экипированного предмета
                if hasattr(item, 'equipped') and item.equipped:
                    equip_text = self.small_font.render("[Экипировано]", True, (106, 176, 76))
                    self.screen.blit(equip_text, (800, y_pos))

    def draw_equipped_items(self, hero):
        """Отрисовка экипированных предметов"""
        if not hero:
            return

        equipped = hero.get_equipped_items()
        if equipped:
            self.draw_panel(20, 550, 400, 120, "ЭКИПИРОВКА")

            for i, item in enumerate(equipped):
                text = self.small_font.render(f"• {item.name}: {item.description}", True, self.colors['text'])
                self.screen.blit(text, (35, 575 + i * 25))