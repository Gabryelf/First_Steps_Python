# skills/skills_data.py - данные навыков

from arena_kombat.skills.base_skill import BaseSkill

# Навыки воина
WARRIOR_SKILLS = {
    'q': BaseSkill(
        name='Сильный удар',
        skill_type='attack',
        energy_cost=15,
        cooldown=30,
        damage_multiplier=1.8
    ),
    'w': BaseSkill(
        name='Блок щитом',
        skill_type='block',
        energy_cost=10,
        cooldown=20
    ),
    'e': BaseSkill(
        name='Ярость',
        skill_type='buff',
        energy_cost=20,
        cooldown=45
    )
}

# Навыки мага
MAGE_SKILLS = {
    'q': BaseSkill(
        name='Огненный шар',
        skill_type='attack',
        energy_cost=20,
        cooldown=25,
        damage_multiplier=2.2
    ),
    'w': BaseSkill(
        name='Ледяная броня',
        skill_type='block',
        energy_cost=15,
        cooldown=35
    ),
    'e': BaseSkill(
        name='Медитация',
        skill_type='buff',
        energy_cost=0,
        cooldown=60
    )
}

# Навыки лучника
ARCHER_SKILLS = {
    'q': BaseSkill(
        name='Точный выстрел',
        skill_type='attack',
        energy_cost=12,
        cooldown=20,
        damage_multiplier=1.5
    ),
    'w': BaseSkill(
        name='Уклонение',
        skill_type='block',
        energy_cost=8,
        cooldown=25
    ),
    'e': BaseSkill(
        name='Град стрел',
        skill_type='attack',
        energy_cost=25,
        cooldown=40,
        damage_multiplier=2.5
    )
}
