# characters/warrior.py - класс воина

from arena_kombat.characters.base_hero import BaseHero
from arena_kombat.skills.skills_data import WARRIOR_SKILLS
from arena_kombat.config.settings import DEFAULT_STATS


class Warrior(BaseHero):
    """Класс воина"""

    def __init__(self, x, y, is_player=True):
        stats = DEFAULT_STATS['warrior'].copy()
        skills = WARRIOR_SKILLS.copy()

        super().__init__(
            x=x,
            y=y,
            name='Воин',
            stats=stats,
            skills=skills,
            sprite_path=None,  # пока без спрайта
            is_player=is_player
        )

        # Специфичные для воина параметры
        self.color = (100, 150, 200) if is_player else (200, 100, 100)
        self.create_placeholder_sprite()

# Аналогично создайте mage.py и archer.py