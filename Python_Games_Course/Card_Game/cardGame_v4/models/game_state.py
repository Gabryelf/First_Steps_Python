from typing import Optional, List, Dict, Any  # Добавляем Any
from .hero import Hero
from .enemy import Enemy
from .item import HealthPotion
from .merchant import Merchant
import random


class GameState:
    """Расширенный менеджер состояния игры"""

    def __init__(self):
        self.hero = None
        self.current_enemy = None
        self.merchant = None  # Добавляем торговца
        self.is_player_turn = True
        self.game_over = False
        self.message_log = []
        self.current_floor = 1
        self.enemies_defeated = 0
        self.player_name = ""
        self.encounter_type = "battle"  # "battle", "merchant"

    def initialize_new_game(self, player_name: str, hero_name: str, hero_class: str):
        """Инициализация новой игры"""
        self.player_name = player_name
        self.hero = Hero(hero_name, hero_class)
        self.current_floor = 1
        self.enemies_defeated = 0
        self.is_player_turn = True
        self.game_over = False
        self.message_log = ["Игра началась!", f"Вы играете за {hero_class} - {hero_name}"]

        self.hero._floor = self.current_floor
        self.hero._enemies_defeated = self.enemies_defeated

        # Стартовые предметы
        self.hero.add_item(HealthPotion())

        self._generate_enemy()
        self.hero.start_turn()

    def load_game(self, player_name: str, save_data: Dict[str, Any]):
        """Загрузка игры из сохранения"""
        # Здесь будет логика загрузки героя из save_data
        # Временно оставляем пустым
        pass

    def _generate_enemy(self):
        """Генерация врага или торговца"""
        # 25% шанс встретить торговца каждые 3 этажа
        if self.current_floor >= 3 and random.random() < 0.25:
            self.encounter_type = "merchant"
            self.merchant = Merchant(self.current_floor)
            self.message_log.append("🎪 Вы встретили бродячего торговца!")
            self.message_log.append("Используйте ←→ для выбора товара, B для покупки")
            return

        self.encounter_type = "battle"
        enemy_names = ["Гоблин", "Скелет", "Орк", "Тролль", "Варвар"]
        base_level = max(1, self.current_floor)

        level_bonus = (self.current_floor - 1) // 3
        enemy_level = base_level + level_bonus

        enemy_name = random.choice(enemy_names)
        self.current_enemy = Enemy(enemy_name, enemy_level)

        self.message_log.append(f"⚔️ Появился {self.current_enemy.name} (Уровень {self.current_enemy.level})!")

    def player_play_card(self, card_index: int) -> str:
        """Игрок играет карту"""
        if not self.is_player_turn or self.game_over:
            return "Сейчас не ваш ход!"

        if not self.hero or not self.current_enemy:
            return "Игра не инициализирована!"

        result = self.hero.play_card(card_index, self.current_enemy)
        self.message_log.append(result)

        self._check_battle_end()
        return result

    def player_use_item(self, item_index: int) -> str:
        """Игрок использует предмет"""
        if not self.is_player_turn or self.game_over:
            return "Сейчас не ваш ход!"

        if not self.hero:
            return "Герой не инициализирован!"

        result = self.hero.use_item(item_index)
        self.message_log.append(result)

        # Использование предмета заканчивает ход
        self.is_player_turn = False
        self.enemy_turn()

        return result

    def end_player_turn(self):
        """Игрок заканчивает ход"""
        if self.is_player_turn and not self.game_over:
            self.is_player_turn = False
            self.message_log.append("Вы закончили ход.")

            # Немедленно запускаем ход врага
            self.enemy_turn()

    def enemy_turn(self):
        """Ход врага"""
        if self.current_enemy and self.current_enemy.is_alive and self.hero:
            result = self.current_enemy.make_turn(self.hero)
            self.message_log.append(result)

            # Проверяем не умер ли герой после атаки врага
            if not self.hero.is_alive:
                self.message_log.append("Вы проиграли!")
                self.game_over = True
                return

            # Если герой выжил, передаем ход обратно игроку
            self.is_player_turn = True

            # Восстанавливаем энергию герою и даем новые карты
            self.hero.start_turn()

            self.message_log.append("Ваш ход! Энергия восстановлена.")

        else:
            # Если враг мертв или нет героя, все равно передаем ход игроку
            self.is_player_turn = True
            if self.hero:
                self.hero.start_turn()

    # В методе _check_battle_end() в game_state.py
    def _check_battle_end(self):
        """Проверка окончания битвы"""
        if not self.hero:
            return

        if self.current_enemy and not self.current_enemy.is_alive:
            # Победа над врагом
            rewards = self.current_enemy.get_rewards()
            self.hero.add_experience(rewards["experience"])
            self.hero.add_gold(rewards["gold"])
            self.enemies_defeated += 1

            # Передаем данные герою для отображения
            self.hero._floor = self.current_floor
            self.hero._enemies_defeated = self.enemies_defeated

            self.message_log.extend([
                f"Вы победили {self.current_enemy.name}!",
                f"Получено: {rewards['experience']} опыта, {rewards['gold']} золота"
            ])

            # Шанс выпадения предмета
            if random.random() < 0.3:  # 30% шанс
                from .item import HealthPotion, EnergyPotion
                item = random.choice([HealthPotion(), EnergyPotion()])
                self.hero.add_item(item)
                self.message_log.append(f"Найден предмет: {item.name}")

            # СОХРАНЕНИЕ ПОСЛЕ ПОБЕДЫ НАД ВРАГОМ
            if hasattr(self, 'repository'):
                hero_data = self.hero.get_save_data()
                game_state_data = self.get_save_data()
                self.repository.save_game(
                    self.player_name,
                    hero_data,
                    game_state_data
                )
                print("Сохранение после победы над врагом")

            # Переход к следующему врагу или уровню
            self.current_floor += 1
            self._generate_enemy()
            self.is_player_turn = True
            if self.hero:
                self.hero.start_turn()

        elif not self.hero.is_alive:
            # Поражение - СОХРАНЕНИЕ СТАТИСТИКИ
            self.message_log.append("Вы проиграли!")
            self.game_over = True

            if hasattr(self, 'repository'):
                game_result = self.get_game_result()
                self.repository.update_player_statistics(self.player_name, game_result)
                print("Статистика обновлена после поражения")

    def get_save_data(self) -> Dict[str, Any]:
        """Получить данные для сохранения"""
        hero_data = self.hero.get_save_data() if self.hero else {}
        return {
            "current_floor": self.current_floor,
            "enemies_defeated": self.enemies_defeated,
            "game_over": self.game_over,
            "is_player_turn": self.is_player_turn,
            "hero_data": hero_data
        }

    def get_game_result(self) -> Dict[str, Any]:
        """Получить результат игры для статистики"""
        if not self.hero:
            return {
                "won": False,
                "level_reached": 0,
                "enemies_defeated": 0,
                "gold_earned": 0,
                "score": 0
            }

        return {
            "won": not self.game_over and self.enemies_defeated > 0,
            "level_reached": self.hero.level,
            "enemies_defeated": self.enemies_defeated,
            "gold_earned": self.hero.gold,
            "score": self._calculate_score()
        }

    def _calculate_score(self) -> int:
        """Расчет очков для лидерборда"""
        if not self.hero:
            return 0
        return (self.hero.level * 100 +
                self.enemies_defeated * 50 +
                self.hero.gold +
                self.current_floor * 25)

    def player_buy_item(self, item_index: int) -> str:
        """Покупка предмета у торговца"""
        if self.encounter_type != "merchant" or not self.merchant:
            return "Сейчас нет торговца!"

        result = self.merchant.buy_item(self.hero, item_index)
        self.message_log.append(result)
        return result

    def leave_merchant(self):
        """Уход от торговца"""
        if self.encounter_type == "merchant":
            self.encounter_type = "battle"
            self.merchant = None
            self._generate_enemy()  # Генерируем следующего врага