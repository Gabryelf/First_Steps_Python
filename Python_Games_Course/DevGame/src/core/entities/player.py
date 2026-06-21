from .base import Unit

class Player(Unit):
    """Класс игрока - главный персонаж, управляемый пользователем."""

    def __init__(self, name: str = "Hero", x: int = 0, y: int = 0):
        super().__init__(name, x, y, health=120)  # У игрока больше здоровья

    def symbol(self) -> str:
        return "@"  # Классический символ игрока в roguelike играх

    def get_actions(self):
        """Возможные действия игрока. Будет расширяться в будущем."""
        return ["move", "interact", "attack"]