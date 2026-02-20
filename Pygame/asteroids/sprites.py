import pygame

background_image = pygame.image.load('sprites/back.png')
background_image = pygame.transform.scale(background_image, (800,600))
player_image = pygame.image.load('sprites/player.png')
asteroid_image = pygame.image.load('sprites/asteroid.png')
asteroid_good_image = pygame.image.load('sprites/asteroid_good.png')
