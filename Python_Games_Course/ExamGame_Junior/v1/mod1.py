import pygame
import time

pygame.init()

catch_sound = pygame.mixer.Sound("../audio/catch.wav")
miss_sound = pygame.mixer.Sound("../audio/miss.wav")

pygame.mixer.music.load("../audio/Bgm-v3.wav")
pygame.mixer.music.play(-1)
music_on = True

catch_sound.play()
time.sleep(5)
miss_sound.play()
time.sleep(5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                music_on = not music_on
                if music_on:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
