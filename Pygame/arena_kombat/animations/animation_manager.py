# animations/animation_manager.py - управление анимациями

import pygame


class AnimationManager:
    """Управление анимациями из спрайт-листа"""

    def __init__(self, sprite_path, animation_config, frame_width=64, frame_height=64):
        self.animation_config = animation_config
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.current_animation = 'idle'
        self.current_frame = 0
        self.frame_timer = 0
        self.animation_finished = False

        # Загрузка спрайт-листа
        if sprite_path:
            try:
                self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            except:
                self.sprite_sheet = None
        else:
            self.sprite_sheet = None

    def set_animation(self, animation_name):
        """Сменить анимацию"""
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.current_frame = 0
            self.frame_timer = 0
            self.animation_finished = False

    def update(self):
        """Обновление анимации"""
        if self.current_animation not in self.animation_config:
            return

        config = self.animation_config[self.current_animation]
        frame_count = config['frames']
        animation_speed = config['speed']

        self.frame_timer += 1

        if self.frame_timer >= animation_speed * 60:
            self.frame_timer = 0
            self.current_frame += 1

            if self.current_frame >= frame_count:
                self.current_frame = 0
                self.animation_finished = True
            else:
                self.animation_finished = False

    def get_current_frame(self):
        """Получить текущий кадр анимации"""
        if not self.sprite_sheet:
            # Создаём заглушку
            surf = pygame.Surface((self.frame_width, self.frame_height))
            surf.fill((100, 100, 100))
            return surf

        config = self.animation_config.get(self.current_animation, {})
        row = config.get('row', 0)

        # Вырезаем кадр из спрайт-листа
        frame_x = self.current_frame * self.frame_width
        frame_y = row * self.frame_height

        frame = self.sprite_sheet.subsurface((frame_x, frame_y, self.frame_width, self.frame_height))
        return frame

    def is_finished(self):
        """Завершена ли анимация"""
        return self.animation_finished
