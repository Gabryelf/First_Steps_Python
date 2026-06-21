from typing import Optional
from .hero import Hero
from .enemy import Enemy


class GameState:
    """Управляет состоянием игры"""

    def __init__(self):
        self.hero: Optional[Hero] = None
        self.current_enemy: Optional[Enemy] = None
        self.is_player_turn = True
        self.game_over = False
        self.message_log = []

    def initialize_game(self, hero_name: str):
        """Инициализация новой игры"""
        self.hero = Hero(hero_name)
        self.current_enemy = Enemy("Гоблин", 30, 10)
        self.is_player_turn = True
        self.game_over = False
        self.message_log = ["Игра началась!", f"Противник: {self.current_enemy.name}"]

        # Добавляем стартовые карты
        from .attack_card import AttackCard
        self.hero.add_card_to_deck(AttackCard("Удар", 8, 1))
        self.hero.add_card_to_deck(AttackCard("Сильный удар", 15, 2))
        self.hero.add_card_to_deck(AttackCard("Удар", 8, 1))
        self.hero.add_card_to_deck(AttackCard("Сильный удар", 15, 2))

        self.hero.start_turn()

    def player_play_card(self, card_index: int) -> str:
        """Игрок играет карту"""
        if not self.is_player_turn or self.game_over:
            return "Сейчас не ваш ход!"

        result = self.hero.play_card(card_index, self.current_enemy)
        self.message_log.append(result)

        # Проверяем победу
        if not self.current_enemy.is_alive:
            self.message_log.append(f"Вы победили {self.current_enemy.name}!")
            self.game_over = True
            return result

        # Передаем ход врагу
        self.is_player_turn = False
        self.enemy_turn()

        return result

    def enemy_turn(self):
        """Ход врага"""
        if self.current_enemy and self.current_enemy.is_alive:
            result = self.current_enemy.make_turn(self.hero)
            self.message_log.append(result)

            # Проверяем поражение
            if not self.hero.is_alive:
                self.message_log.append("Вы проиграли!")
                self.game_over = True
            else:
                self.is_player_turn = True
                self.hero.start_turn()