# skills/base_skill.py - базовый класс навыка

import random


class BaseSkill:
    """Базовый класс для всех навыков"""

    def __init__(self, name, skill_type, energy_cost, cooldown, damage_multiplier=1.0, effect=None):
        self.name = name
        self.skill_type = skill_type  # 'attack', 'block', 'buff'
        self.energy_cost = energy_cost
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.damage_multiplier = damage_multiplier
        self.effect = effect

    def use(self, caster, target):
        """Использование навыка"""
        if self.current_cooldown > 0:
            return {
                'success': False,
                'message': f'{self.name} на перезарядке! ({self.current_cooldown} сек)'
            }

        if caster.stats['energy'] < self.energy_cost:
            return {
                'success': False,
                'message': f'Недостаточно энергии! Нужно {self.energy_cost}'
            }

        caster.stats['energy'] -= self.energy_cost
        self.current_cooldown = self.cooldown

        if self.skill_type == 'attack':
            return self.perform_attack(caster, target)
        elif self.skill_type == 'block':
            return self.perform_block(caster)
        elif self.skill_type == 'buff':
            return self.perform_buff(caster)

    def update_cooldown(self):
        """Обновление кулдауна"""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

    def perform_attack(self, caster, target):
        """Выполнение атаки"""
        base_damage = caster.stats['attack'] * self.damage_multiplier

        # Шанс крита
        is_crit = random.random() < caster.stats['crit_chance']
        if is_crit:
            base_damage *= 1.5

        # Шанс уворота цели
        is_dodge = random.random() < target.stats['dodge_chance']
        if is_dodge:
            return {
                'success': True,
                'damage': 0,
                'is_dodge': True,
                'message': f'{target.name} уклонился от {self.name}!'
            }

        # Расчёт защиты
        damage_reduction = target.stats['defense'] / (target.stats['defense'] + 100)
        final_damage = int(base_damage * (1 - damage_reduction))
        final_damage = max(1, final_damage)  # минимум 1 урон

        target.stats['hp'] -= final_damage

        message = f'{self.name} нанёс {final_damage} урона!'
        if is_crit:
            message = f'КРИТ! {message}'

        return {
            'success': True,
            'damage': final_damage,
            'is_crit': is_crit,
            'message': message
        }

    def perform_block(self, caster):
        """Выполнение блока"""
        # Блок увеличивает защиту временно
        caster.stats['defense_bonus'] = 20
        return {
            'success': True,
            'message': f'{caster.name} использует {self.name}, защита увеличена!'
        }

    def perform_buff(self, caster):
        """Выполнение баффа"""
        # Бафф увеличивает атаку временно
        caster.stats['attack_bonus'] = 10
        return {
            'success': True,
            'message': f'{caster.name} использует {self.name}, атака увеличена!'
        }