# game/arena.py - арена боя

import pygame
import random
from arena_kombat.config.settings import *


class Arena:
    """Класс арены, управляющий боем"""

    def __init__(self, screen, player, enemy, save_data):
        self.screen = screen
        self.player = player
        self.enemy = enemy
        self.save_data = save_data
        self.battle_log = []
        self.log_timer = 0
        self.battle_result = None  # None, 'player_win', 'enemy_win'
        self.result_timer = 0

        # AI таймер
        self.ai_timer = 0

        # Фон
        self.background_color = (30, 30, 40)

    def handle_event(self, event):
        """Обработка ввода игрока"""
        if self.battle_result:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 'back_to_menu'
            return None

        if event.type == pygame.KEYDOWN:
            # Движение
            if event.key == pygame.K_LEFT:
                self.player.move_left()
            elif event.key == pygame.K_RIGHT:
                self.player.move_right()
            elif event.key == pygame.K_UP:
                self.player.jump()

            # Навыки
            elif event.key == pygame.K_q:
                self.use_player_skill('q')
            elif event.key == pygame.K_w:
                self.use_player_skill('w')
            elif event.key == pygame.K_e:
                self.use_player_skill('e')

        return None

    def use_player_skill(self, skill_key):
        """Использование навыка игроком"""
        result = self.player.use_skill(skill_key, self.enemy)
        if result:
            self.add_log(result.get('message', f'Использован навык {skill_key.upper()}'))

            # Проверка на победу
            if self.enemy.stats['hp'] <= 0:
                self.end_battle('player_win')

    def ai_decision(self):
        """AI принятие решения"""
        # Простой AI: случайное действие
        actions = ['idle', 'move_left', 'move_right', 'attack']

        # Атакуем, если есть энергия и дистанция подходящая
        distance = abs(self.player.x - self.enemy.x)

        if distance < 80:
            # Близко - атакуем
            for skill_key in ['q', 'w', 'e']:
                skill = self.enemy.skills.get(skill_key)
                if skill and skill.skill_type == 'attack':
                    if self.enemy.stats['energy'] >= skill.energy_cost:
                        result = self.enemy.use_skill(skill_key, self.player)
                        if result:
                            self.add_log(result.get('message', f'Враг использует {skill_key.upper()}'))
                            if self.player.stats['hp'] <= 0:
                                self.end_battle('enemy_win')
                            return
        elif distance > 200:
            # Далеко - идём вперёд
            if self.enemy.x < self.player.x:
                self.enemy.move_right()
            else:
                self.enemy.move_left()
        else:
            # Случайное движение
            if random.random() < 0.3:
                if random.random() < 0.5:
                    self.enemy.move_left()
                else:
                    self.enemy.move_right()

    def add_log(self, message):
        """Добавить сообщение в лог боя"""
        self.battle_log.append(message)
        if len(self.battle_log) > 5:
            self.battle_log.pop(0)
        self.log_timer = 60

    def end_battle(self, winner):
        """Завершение боя"""
        self.battle_result = winner
        self.result_timer = 120  # пауза перед возвратом в меню

        if winner == 'player_win':
            self.save_data['cups'] += 50
            from save_system import SaveSystem
            SaveSystem.save_game(self.save_data)
        elif winner == 'enemy_win':
            self.save_data['cups'] = max(0, self.save_data['cups'] - 25)
            from save_system import SaveSystem
            SaveSystem.save_game(self.save_data)

    def update(self):
        """Обновление арены"""
        if self.battle_result:
            self.result_timer -= 1
            if self.result_timer <= 0:
                return self.battle_result
            return None

        # Обновление героев
        self.player.update()
        self.enemy.update()

        # AI противника
        self.ai_timer += 1
        if self.ai_timer >= 30:  # раз в 0.5 секунды
            self.ai_timer = 0
            self.ai_decision()

        # Проверка на смерть
        if self.player.stats['hp'] <= 0:
            self.end_battle('enemy_win')
        elif self.enemy.stats['hp'] <= 0:
            self.end_battle('player_win')

        return None

    def draw(self):
        """Отрисовка арены"""
        # Фон
        self.screen.fill(self.background_color)

        # Земля
        pygame.draw.rect(self.screen, (100, 80, 60), (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))

        # Герои
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        # Лог боя
        if self.log_timer > 0:
            self.log_timer -= 1
            font = pygame.font.Font(None, 24)
            y = SCREEN_HEIGHT - 80
            for message in self.battle_log:
                text = font.render(message, True, WHITE)
                self.screen.blit(text, (20, y))
                y += 25

        # Подсказки по управлению
        if not self.battle_result:
            font = pygame.font.Font(None, 20)
            controls = [
                "← → - движение",
                "↑ - прыжок",
                "Q/W/E - навыки"
            ]
            y = SCREEN_HEIGHT - 60
            for text in controls:
                control_text = font.render(text, True, GRAY)
                self.screen.blit(control_text, (SCREEN_WIDTH - 180, y))
                y += 20

        # Результат боя
        if self.battle_result:
            font = pygame.font.Font(None, 48)
            if self.battle_result == 'player_win':
                text = font.render("ПОБЕДА!", True, GREEN)
            else:
                text = font.render("ПОРАЖЕНИЕ!", True, RED)

            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

            hint_font = pygame.font.Font(None, 24)
            hint = hint_font.render("Нажмите ПРОБЕЛ для продолжения", True, WHITE)
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(hint, hint_rect)