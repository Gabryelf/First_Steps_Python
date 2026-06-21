from .card import Card
from .entity import Entity


class AttackCard(Card):
    """Конкретная карта атаки"""

    def __init__(self, name: str, damage: int, energy_cost: int = 1):
        description = f"Наносит {damage} урона"
        super().__init__(name, description, energy_cost)
        self.damage = damage

    def play(self, caster: Entity, target: Entity = None) -> str:
        if target:
            target.take_damage(self.damage)
            return f"{caster.name} использует {self.name} и наносит {self.damage} урона {target.name}!"
        return "Нет цели для атаки!"