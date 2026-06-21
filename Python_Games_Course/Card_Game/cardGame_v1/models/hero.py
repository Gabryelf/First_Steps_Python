from typing import List, Dict
from .entity import Entity
from .card import Card


class Hero(Entity):
    """Класс героя игрока"""

    def __init__(self, name: str, max_health: int = 100):
        super().__init__(name, max_health)
        self.energy = 3
        self.max_energy = 3
        self._deck: List[Card] = []
        self._hand: List[Card] = []

    def get_available_actions(self) -> List[str]:
        actions = ["закончить ход"]
        if any(card.energy_cost <= self.energy for card in self._hand):
            actions.append("использовать карту")
        return actions

    def add_card_to_deck(self, card: Card):
        """Добавить карту в колоду"""
        self._deck.append(card)

    def draw_hand(self, cards_count: int = 5):
        """Взять карты в руку (упрощенная версия)"""
        self._hand = self._deck[:cards_count]  # В реальной игре нужно перемешивать

    def get_hand(self) -> List[Card]:
        """Получить карты в руке"""
        return self._hand.copy()

    def play_card(self, card_index: int, target: Entity = None) -> str:
        """Сыграть карту из руки"""
        if 0 <= card_index < len(self._hand):
            card = self._hand[card_index]
            if self.energy >= card.energy_cost:
                self.energy -= card.energy_cost
                result = card.play(self, target)
                # Убираем карту из руки (в реальной игре может быть по-другому)
                self._hand.pop(card_index)
                return result
            return "Недостаточно энергии!"
        return "Неверный индекс карты!"

    def start_turn(self):
        """Начало хода героя"""
        self.energy = self.max_energy
        self.draw_hand()