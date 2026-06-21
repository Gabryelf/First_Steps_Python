import time
from typing import Optional, List
import pygame

from .renderer import Renderer, PygameRenderer
from .game_state import GameState
from .wave_manager import WaveManager
from .battle_manager import BattleManager
from .entity_renderer import EntityRenderer
from ..entities.tower import Tower
from ..ui.components import Button, InfoPanel
from ..ui.upgrade_ui import UpgradePanel
from ..database.base_database import MockDatabase
from ..systems.upgrade_system import UpgradeSystem
from ..utils.config import config
from ..utils.logger import logger
from .enemy_spawner import EnemySpawner
from client.game_client import GameClient


class GameEngine:
    """
    Основной игровой движок, управляющий всем циклом игры.
    Координирует работу всех систем игры.
    """

    def __init__(self) -> None:
        # Инициализация всех систем в конструкторе - понятная структура
        self._initialize_systems()
        self._initialize_state()
        self.game_client = GameClient()  # Добавляем клиент для сервера
        self.authenticated = False

    def _initialize_systems(self) -> None:
        """Инициализация игровых систем"""
        if not self._check_authentication():
            return False

        if not self._initialize_graphics():
            return False

        self._load_server_data()  # Загружаем данные с сервера
        # Системы рендеринга
        self.renderer: Optional[Renderer] = None
        self.entity_renderer: Optional[EntityRenderer] = None
        self.clock: Optional[pygame.time.Clock] = None

        # Игровые системы
        self.game_state: Optional[GameState] = None
        self.wave_manager: Optional[WaveManager] = None
        self.battle_manager: Optional[BattleManager] = None
        self.tower: Optional[Tower] = None
        self.upgrade_system: Optional[UpgradeSystem] = None
        self.database: Optional[MockDatabase] = None
        self.enemy_spawner: Optional[EnemySpawner] = None  # ДОБАВЛЯЕМ ЗДЕСЬ

        # UI компоненты
        self.ui_components: List[Button | InfoPanel | UpgradePanel] = []
        self.upgrade_panel: Optional[UpgradePanel] = None

    def _check_authentication(self) -> bool:
        """Проверка аутентификации пользователя"""
        # Здесь можно добавить UI для входа/регистрации
        # Пока используем mock-аутентификацию для тестов
        if config.USE_MOCK_AUTH:
            self.authenticated = True
            return True

        # Реальная аутентификация
        # return self._show_login_screen()
        return True

    def _load_server_data(self):
        """Загрузка данных игрока с сервера"""
        if not self.authenticated:
            return

        progress = self.game_client.load_game_progress()
        if progress:
            self._apply_server_progress(progress)

    def _save_to_server(self):
        """Сохранение прогресса на сервер"""
        if not self.authenticated:
            return

        game_data = {
            "coins": self.game_state.player_progress.coins,
            "diamonds": self.game_state.player_progress.diamonds,
            "score": self.game_state.player_progress.score,
            "current_wave": self.game_state.player_progress.current_wave,
            "enemies_defeated": self.game_state.player_progress.enemies_defeated,
            "upgrades": self.upgrade_system.save_upgrades()
        }

        self.game_client.save_game_progress(game_data)
    def _initialize_state(self) -> None:
        """Инициализация состояния игры"""
        self.running: bool = False
        self.current_player_id: str = "test_player_001"

        # Статистика производительности
        self.frame_count: int = 0
        self.fps: float = 0.0
        self.last_fps_update: float = time.time()

    def initialize(self) -> bool:
        """Инициализация игрового движка"""
        logger.info("Initializing game engine...")

        if not self._initialize_graphics():
            return False

        self._initialize_game_systems()
        self._initialize_database()
        self._create_user_interface()

        # ПРИНУДИТЕЛЬНАЯ ПРОВЕРКА СИСТЕМ
        systems_ok = all([
            self.game_state is not None,
            self.wave_manager is not None,
            self.battle_manager is not None,
            self.tower is not None,
            self.upgrade_system is not None,
            self.enemy_spawner is not None
        ])

        if not systems_ok:
            logger.error("❌ Some game systems failed to initialize!")
            return False

        logger.info("✅ Game systems initialized successfully")
        return True

    def _initialize_graphics(self) -> bool:
        """Инициализация графических систем"""
        self.renderer = PygameRenderer()
        if not self.renderer.initialize():
            logger.error("Failed to initialize renderer")
            return False

        self.clock = pygame.time.Clock()
        self.entity_renderer = EntityRenderer()
        return True

    def _initialize_game_systems(self) -> None:
        """Инициализация игровых систем"""
        self.game_state = GameState()
        self.wave_manager = WaveManager()
        self.battle_manager = BattleManager()
        self.tower = Tower()
        self.upgrade_system = UpgradeSystem()
        self.enemy_spawner = EnemySpawner()

        # Связываем BattleManager с EntityRenderer для эффектов
        if self.battle_manager and self.entity_renderer:
            self.battle_manager.set_entity_renderer(self.entity_renderer)

        logger.info("✅ All game systems initialized")

    def _initialize_database(self) -> None:
        """Инициализация базы данных"""
        self.database = MockDatabase()
        if not self.database.connect():
            logger.warning("Failed to connect to database, using mock data")
        else:
            self._load_player_data()

    def _create_user_interface(self) -> None:
        """Создание пользовательского интерфейса"""
        # Основные UI компоненты
        start_button = Button(
            (config.SCREEN_WIDTH // 2 - 100, config.SCREEN_HEIGHT // 2, 200, 50),
            "Start Battle",
            self._on_start_battle
        )

        info_panel = InfoPanel((10, 10, 200, 150))

        # Панель улучшений
        self.upgrade_panel = UpgradePanel((config.SCREEN_WIDTH - 320, 100, 300, 500))
        self.upgrade_panel.set_systems(self.upgrade_system, self.tower, self.game_state)
        self.upgrade_panel.visible = False

        self.ui_components = [start_button, info_panel, self.upgrade_panel]

    def _load_player_data(self) -> None:
        """Загрузка данных игрока из базы данных"""
        if not self.database:
            return

        player_data = self.database.load_player_data(self.current_player_id)
        if player_data and 'upgrades' in player_data:
            self.upgrade_system.load_upgrades(player_data['upgrades'])
            logger.info("Player upgrades loaded from database")

    def _save_player_data(self) -> None:
        """Сохранение данных игрока в базу данных"""
        if not self.database or not self.game_state or not self.tower:
            return

        player_data = {
            'player_id': self.current_player_id,
            'upgrades': self.upgrade_system.save_upgrades(),
            'high_score': self.game_state.player_progress.score,
            'level': self.tower.level,
            'last_save': time.time()
        }

        if self.database.save_player_data(self.current_player_id, player_data):
            logger.debug("Player data saved successfully")
        else:
            logger.error("Failed to save player data")

    def _on_start_battle(self) -> None:
        """Обработчик начала битвы"""
        if not self.game_state or not self.wave_manager:
            return

        self.game_state.start_battle()
        # Принудительно начинаем волну 1
        self.wave_manager.start_wave(1)
        self._update_ui_for_battle()
        logger.info("Battle started with wave 1")

    def _update_ui_for_battle(self) -> None:
        """Обновление UI при начале битвы"""
        for component in self.ui_components:
            if isinstance(component, Button) and component.text == "Start Battle":
                component.visible = False
            elif isinstance(component, UpgradePanel):
                component.visible = True

        logger.info("UI updated for battle mode")

    def run(self) -> None:
        """Запуск основного игрового цикла"""
        if not self.initialize():
            logger.error("Cannot run game - initialization failed")
            return

        self.running = True
        logger.info("Starting main game loop")
        self._game_loop()

    def _game_loop(self) -> None:
        """Основной игровой цикл"""
        last_time = time.time()

        while self.running:
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time

            self._handle_events()
            self._update_game_state(delta_time)
            self._render_frame()
            self._update_performance_stats()

            # Контроль FPS
            if self.clock:
                self.clock.tick(config.FPS)

        self._shutdown()

    def _handle_events(self) -> None:
        """Обработка событий ввода"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                logger.info("Quit event received")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
                logger.info("Escape key pressed - quitting")
            else:
                self._handle_ui_events(event)

    def _handle_ui_events(self, event: pygame.event.Event) -> None:
        """Обработка событий UI"""
        for component in self.ui_components:
            if component.handle_event(event):
                break

    def _update_game_state(self, delta_time: float) -> None:
        """Обновление состояния игры"""
        self.frame_count += 1

        if not self.game_state or not self.game_state.game_active:
            return

        # ПРОВЕРКА СИСТЕМ ПЕРЕД ОБНОВЛЕНИЕМ
        if not all([self.wave_manager, self.battle_manager, self.enemy_spawner]):
            logger.error(f"❌ Missing systems: wave_manager={self.wave_manager is not None}, "
                         f"battle_manager={self.battle_manager is not None}, "
                         f"enemy_spawner={self.enemy_spawner is not None}")
            return

        self._update_waves(delta_time)
        self._update_battle(delta_time)
        self._handle_auto_save()

    def _update_waves(self, delta_time: float) -> None:
        """Обновление волн врагов"""
        # УПРОЩАЕМ ПРОВЕРКУ
        if not self.wave_manager:
            logger.error("❌ WaveManager is None!")
            return
        if not self.battle_manager:
            logger.error("❌ BattleManager is None!")
            return
        if not self.enemy_spawner:
            logger.error("❌ EnemySpawner is None!")
            return

        enemies_to_spawn = self.wave_manager.update(delta_time, self.game_state)

        logger.info(f"🔍 Wave update: {len(enemies_to_spawn)} enemies to spawn")
        logger.info(f"🔍 Wave state: in_progress={self.wave_manager.wave_in_progress}, "
                    f"current_wave={self.wave_manager.current_wave}")

        for enemy_type in enemies_to_spawn:
            # Получаем случайную позицию спавна на периметре
            spawn_position = self.enemy_spawner.get_random_spawn_position()
            logger.info(f"🎯 Spawning {enemy_type} at {spawn_position}")

            enemy = self.battle_manager.spawn_enemy(enemy_type, spawn_position)
            logger.info(
                f"✅ Successfully spawned {enemy_type}. Active enemies: {len(self.battle_manager.active_enemies)}")

    def _update_battle(self, delta_time: float) -> None:
        """Обновление боевой системы"""
        if not self.battle_manager or not self.tower or not self.game_state:
            logger.error("❌ Missing systems for battle update")
            return

        # ОТЛАДКА: проверяем состояние перед обновлением
        logger.info(f"🔄 Battle update: {len(self.battle_manager.active_enemies)} active enemies")

        defeated_enemies = self.battle_manager.update(delta_time, self.tower, self.game_state, self.wave_manager)

        # Начисление очков за побежденных врагов
        for enemy in defeated_enemies:
            self.game_state.player_progress.score += enemy.type.reward * 10
            logger.info(f"🎯 Enemy defeated: {enemy.type.name}")

    def _handle_auto_save(self) -> None:
        """Обработка автосохранения"""
        if self.frame_count % (120 * config.FPS) == 0:
            self._save_player_data()

    def _render_frame(self) -> None:
        """Отрисовка кадра"""
        if not self.renderer:
            return

        self.renderer.clear_screen()
        self._render_game_scene()
        self._render_ui()
        self._render_debug_info()
        self.renderer.update_display()

    def _render_game_scene(self) -> None:
        """Отрисовка игровой сцены"""
        if not self.game_state:
            return

        if self.game_state.current_state.name == "LOBBY":
            self._render_lobby_scene()
        elif self.game_state.current_state.name == "BATTLE":
            self._render_battle_scene()

    def _render_lobby_scene(self) -> None:
        """Отрисовка сцены лобби"""
        if not self.renderer:
            return

        # Заголовок
        title_text = "Idle Tower Defense - Lobby"
        self.renderer.draw_text(title_text,
                                (config.SCREEN_WIDTH // 2 - 200, 100),
                                (255, 255, 255), 36)

        # Центральная башня
        self.renderer.draw_circle(config.screen_center, 60, (70, 130, 180))

    def _render_battle_scene(self) -> None:
        """Отрисовка сцены битвы"""
        if not self.renderer:
            return

        # Боевые сущности
        if (self.entity_renderer and self.battle_manager and self.tower):
            self.entity_renderer.draw_battle_entities(
                self.renderer.screen,
                self.tower,
                self.battle_manager.active_enemies,
                self.battle_manager.active_projectiles
            )

        # ОТЛАДКА: рисуем пути врагов
        if self.battle_manager:
            for enemy in self.battle_manager.active_enemies:
                if len(enemy.path) > 1:
                    # Рисуем линию от врага к следующей точке пути
                    next_point = enemy.path[enemy.current_path_index + 1]
                    pygame.draw.line(self.renderer.screen, (255, 0, 0),
                                     (int(enemy.position[0]), int(enemy.position[1])),
                                     (int(next_point[0]), int(next_point[1])), 1)

                    # Рисуем точки пути
                    for point in enemy.path:
                        pygame.draw.circle(self.renderer.screen, (255, 255, 0),
                                           (int(point[0]), int(point[1])), 3)

        # Радиус атаки башни
        if self.tower:
            attack_range = self.tower.current_stats.attack_range
            self.renderer.draw_circle(self.tower.position, attack_range,
                                      (255, 255, 255), 1)

        # Информация о битве
        if self.game_state and self.battle_manager:
            self._render_battle_info()

        # Отладочная информация: враги у башни
        if self.battle_manager:
            enemies_at_tower = self.battle_manager.get_enemies_at_tower()
            active_enemies = len(self.battle_manager.active_enemies)

            debug_text = f"Active enemies: {active_enemies}, At tower: {len(enemies_at_tower)}"
            self.renderer.draw_text(debug_text, (10, 70), (255, 255, 0), 20)

            if self.wave_manager:
                wave_info = f"Wave: {self.wave_manager.current_wave}, Spawned: {self.wave_manager.enemies_spawned}"
                self.renderer.draw_text(wave_info, (10, 90), (255, 255, 0), 20)

    def _render_battle_info(self) -> None:
        """Отрисовка информации о битве"""
        wave_text = f"Wave: {self.game_state.player_progress.current_wave}"
        self.renderer.draw_text(wave_text, (config.SCREEN_WIDTH // 2 - 50, 20),
                                (255, 255, 255), 28)

        enemies_text = f"Enemies: {self.battle_manager.get_enemy_count()}"
        self.renderer.draw_text(enemies_text, (config.SCREEN_WIDTH // 2 - 50, 50),
                                (255, 255, 255), 24)

        # Здоровье башни
        if self.tower:
            health_text = f"Tower HP: {int(self.tower.health)}/{int(self.tower.max_health)}"
            health_color = (0, 255, 0) if self.tower.health_ratio > 0.3 else (255, 165, 0)
            self.renderer.draw_text(health_text, (config.SCREEN_WIDTH // 2 - 50, 80),
                                    health_color, 24)

        # Отладочная информация об уроне
        if self.battle_manager and self.battle_manager.active_projectiles:
            projectiles_text = f"Projectiles: {len(self.battle_manager.active_projectiles)}"
            self.renderer.draw_text(projectiles_text, (10, 100), (255, 255, 0), 20)

        # Информация о текущей цели башни
        if self.tower and self.tower.current_target:
            target_text = f"Target: {self.tower.current_target.type.name}"
            self.renderer.draw_text(target_text, (10, 120), (255, 200, 0), 20)

        # Информация о волне (отладка)
        if self.wave_manager and self.wave_manager.wave_in_progress:
            wave_config = self.wave_manager.wave_config_manager.get_wave_config(self.wave_manager.current_wave)
            wave_info = f"Wave Progress: {self.wave_manager.enemies_spawned}/{wave_config.total_enemies}"
            self.renderer.draw_text(wave_info, (10, 100), (255, 255, 0), 20)

    def _render_ui(self) -> None:
        """Отрисовка пользовательского интерфейса"""
        if not self.renderer:
            return

        for component in self.ui_components:
            if hasattr(component, 'draw'):
                if type(component).__name__ == 'InfoPanel' and self.game_state:
                    component.draw(self.renderer.screen, self.game_state)
                else:
                    component.draw(self.renderer.screen)

    def _render_debug_info(self) -> None:
        """Отрисовка отладочной информации"""
        if not self.renderer:
            return

        fps_text = f"FPS: {self.fps:.1f}"
        self.renderer.draw_text(fps_text, (10, 10), (0, 255, 0), 24)

        frame_text = f"Frames: {self.frame_count}"
        self.renderer.draw_text(frame_text, (10, 40), (0, 255, 0), 24)



    def _update_performance_stats(self) -> None:
        """Обновление статистики производительности"""
        current_time = time.time()
        if current_time - self.last_fps_update >= 1.0:
            self.fps = self.clock.get_fps() if self.clock else 0
            self.last_fps_update = current_time

    def _shutdown(self) -> None:
        """Корректное завершение работы"""
        self._save_player_data()

        if self.database:
            self.database.disconnect()

        logger.info("Game engine shut down successfully")
        pygame.quit()