import pygame

pygame.mixer.init()
fruit_eat = pygame.mixer.Sound("sounds/sound_eat.ogg")
fruit_eat.set_volume(0.5)
main_music = pygame.mixer.Sound("sounds/main_music.ogg")
main_music.set_volume(0.1)
