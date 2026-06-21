from .base import Unit


class NPC(Unit):

    def __init__(self, name: str, x: int, y: int, dialog: str = "Hello!"):
        super().__init__(name, x, y, health=80)
        self.dialog = dialog

    def symbol(self) -> str:
        return "N"  # Символ NPC

    def interact(self):
        return f"{self.name}: {self.dialog}"
