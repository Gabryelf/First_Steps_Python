from typing import List, Dict, Any, Tuple
from client.src.entities.enemy import Enemy
from client.src.entities.projectile import Projectile
from client.src.utils.config import config
from client.src.utils.logger import logger


class BattleManager:
    """Менеджер боевой системы - обрабатывает все взаимодействия в битве"""

    def __init__(self):
        self.active_enemies: List[Enemy] = []
        self.active_projectiles: List[Projectile] = []
        self.defeated_enemies = 0
        self.entity_renderer = None

        logger.info("BattleManager initialized")

    def set_entity_renderer(self, entity_renderer):
        """Установка ссылки на рендерер для эффектов"""
        self.entity_renderer = entity_renderer

    def spawn_enemy(self, enemy_type: str, spawn_position: Tuple[float, float]) -> Enemy:
        """Создание нового врага в указанной позиции"""
        # Создаем путь от точки спавна к башне
        path = [spawn_position, config.screen_center]
        enemy = Enemy(enemy_type, path)
        self.active_enemies.append(enemy)
        logger.debug(f"Spawned {enemy_type} at position {spawn_position}")
        return enemy

    def update(self, delta_time: float, tower, game_state, wave_manager=None) -> List[Enemy]:
        """Обновление всей боевой системы. Возвращает убитых врагов"""
        defeated_enemies = []

        # Обновление врагов
        self._update_enemies(delta_time, tower, game_state)

        # Обновление снарядов от башни
        if tower and tower.is_alive():
            new_projectiles = tower.update(delta_time, self.active_enemies)
            self.active_projectiles.extend(new_projectiles)

        # Обновление снарядов и проверка попаданий
        self._update_projectiles()

        # Сбор убитых врагов (только тех, кто умер от урона)
        for enemy in self.active_enemies[:]:
            if not enemy.is_alive():
                self.active_enemies.remove(enemy)
                defeated_enemies.append(enemy)
                self.defeated_enemies += 1

                # Уведомляем WaveManager о убитом враге
                if wave_manager:
                    wave_manager.on_enemy_defeated()

                # Награда за убийство
                if game_state and game_state.player_progress:
                    reward = enemy.type.reward
                    experience = enemy.type.experience
                    game_state.player_progress.add_coins(reward)
                    game_state.player_progress.enemies_defeated += 1
                    if tower:
                        tower.add_experience(experience)

                logger.debug(f"Enemy defeated by damage! Reward: {reward} coins, {experience} XP")

        return defeated_enemies

    def _update_enemies(self, delta_time: float, tower, game_state):
        """Обновление позиций врагов"""
        for enemy in self.active_enemies[:]:
            reached_end = enemy.update(delta_time)

            if reached_end and enemy.is_alive():
                # Враг достиг башни - наносим урон каждый кадр
                if tower and tower.is_alive():
                    damage = max(1, enemy.type.health // 50)  # Небольшой постоянный урон
                    tower_destroyed = tower.take_damage(damage)

                    if tower_destroyed:
                        if game_state:
                            game_state.end_battle(victory=False)

    def _update_projectiles(self):
        """Обновление снарядов и проверка попаданий"""
        active_projectiles = []

        for projectile in self.active_projectiles:
            # Обновляем позицию снаряда
            target_reached = projectile.update()

            if target_reached and projectile.active:
                # Снаряд уже нанес урон в методе update() Projectile
                # Здесь только добавляем визуальный эффект
                if self.entity_renderer:
                    self.entity_renderer.add_hit_effect(
                        projectile.target.center_position,
                        projectile.damage
                    )

                projectile.active = False

            # Добавляем снаряд в список только если он активен
            if projectile.active:
                active_projectiles.append(projectile)

        self.active_projectiles = active_projectiles

    def get_enemy_count(self) -> int:
        """Количество активных врагов"""
        return len(self.active_enemies)

    def get_enemies_at_tower(self) -> List[Enemy]:
        """Получение врагов, достигших башни"""
        return [enemy for enemy in self.active_enemies if enemy.reached_end and enemy.is_alive()]