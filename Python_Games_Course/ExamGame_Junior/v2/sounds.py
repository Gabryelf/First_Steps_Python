import pygame


class SoundManager:
    def __init__(self):
        self.catch_sound = pygame.mixer.Sound("audio/catch.wav")
        self.miss_sound = pygame.mixer.Sound("audio/miss.wav")
        pass

    def play_catch(self):
        if hasattr(self, 'catch_sound'):
            self.catch_sound.play()
        pass

    def play_miss(self):
        if hasattr(self, 'miss_sound'):
           self.miss_sound.play()
        pass
    