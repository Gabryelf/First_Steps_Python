from .card import Card
from .entity import Entity


class DefenseCard(Card):
    """Карта защиты"""

    def __init__(self, name: str, block: int, energy_cost: int = 1):
        description = f"Блокирует {block} урона"
        super().__init__(name, description, energy_cost)
        self.block = block

    def play(self, caster: Entity, target: Entity = None) -> str:
        # В этой версии просто возвращаем сообщение
        # В будущем можно добавить систему временной защиты
        return f"{caster.name} использует {self.name} и готовится к защите!"