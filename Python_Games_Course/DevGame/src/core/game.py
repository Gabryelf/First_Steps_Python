from typing import List, Dict, Any


class GameController:
    """
    Главный контроллер игры. Отвечает за:
    - Управление игровым циклом
    - Обработку пользовательского ввода
    - Координацию между различными компонентами
    - Состояние игры
    """

    def __init__(self, map_width: int = 10, map_height: int = 8):
        from core import GameMap
        self.game_map = GameMap(map_width, map_height)
        from core.entities import Player
        self.player = Player("Hero", 1, 1)  # Стартовая позиция игрока
        from core.entities import NPC
        self.npcs: List[NPC] = [
            NPC("Old Sage", 3, 3, "Welcome to our world!"),
            NPC("Guard", 5, 5, "No trespassing!")
        ]
        self.is_running = True

        # Регистрируем обработчики команд
        self.commands: Dict[str, Any] = {
            'w': self._move_up,
            'a': self._move_left,
            's': self._move_down,
            'd': self._move_right,
            'q': self._quit_game,
            'i': self._interact
        }

    def _move_up(self):
        return self.player.move(0, -1, self.game_map)

    def _move_left(self):
        return self.player.move(-1, 0, self.game_map)

    def _move_down(self):
        return self.player.move(0, 1, self.game_map)

    def _move_right(self):
        return self.player.move(1, 0, self.game_map)

    def _quit_game(self):
        self.is_running = False
        return True

    def _interact(self):
        """Взаимодействие с ближайшими NPC"""
        px, py = self.player.position
        for npc in self.npcs:
            nx, ny = npc.position
            # Проверяем соседние клетки
            if abs(px - nx) <= 1 and abs(py - ny) <= 1:
                print(f"\n{npc.interact()}")
                return True
        print("\nNo one to interact with nearby.")
        return True


    def process_input(self) -> bool:
        """Обработка пользовательского ввода. Возвращает True если игра должна продолжиться."""
        print("\nCommand [WASD to move, I-interact, Q-quit]: ", end='', flush=True)
        key = self._get_key().lower()

        if key in self.commands:
            return self.commands[key]()
        else:
            print(f"\nUnknown command: {key}")
            return True

    def render(self):
        """Отрисовка игрового состояния"""
        print("\n" + "=" * 40)

        # Рендерим карту с персонажами
        for y in range(self.game_map.height):
            row = []
            for x in range(self.game_map.width):
                # Проверяем, есть ли здесь игрок
                if (x, y) == self.player.position:
                    row.append(self.player.symbol())
                else:
                    # Проверяем, есть ли здесь NPC
                    npc_here = None
                    for npc in self.npcs:
                        if (x, y) == npc.position:
                            npc_here = npc
                            break

                    if npc_here:
                        row.append(npc_here.symbol())
                    else:
                        row.append(str(self.game_map.get_tile(x, y)))
            print(' '.join(row))

        # Статусная информация
        print(f"\nPlayer: {self.player}")
        print(f"Position: {self.player.position}")

    def run(self):
        """Главный игровой цикл"""
        print("Welcome to the Game!")
        print("Controls: WASD - movement, I - interact, Q - quit")

        while self.is_running:
            self.render()
            self.is_running = self.process_input()

        print("\nThanks for playing! Goodbye!")