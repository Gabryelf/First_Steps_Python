import pygame
import consts
from Asteroid import Asteroid
from Player import Player
from RenderEngine import RenderEngine
from PhysicEngine import PhysicEngine
from ScoreController import ScoreController


class Game():
    render_engine = RenderEngine()
    player = Player(150,150)
    score_count = ScoreController()
    clock = pygame.time.Clock()
    is_end = False
    asteroid_spawn_rate = 1
    asteroids = []
    asteroid_speed = 9
    asteroid_speed_ax = 0.01

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_end = True

    def game_logic(self):
        if self.tick_count >= 40:
            self.asteroid_speed += self.asteroid_speed_ax
            for i in range(int(self.asteroid_spawn_rate)):
                self.asteroids.append(Asteroid(self.asteroid_speed))
            self.tick_count = 0
            self.asteroid_spawn_rate += 0.3
        for index,asteroid in enumerate(self.asteroids) :
            asteroid.move()
            if PhysicEngine.collide_with_left_border(asteroid) or PhysicEngine.collide(self.player, asteroid):
                delastr = self.asteroids.pop(index)
                if PhysicEngine.collide(self.player, asteroid):
                    if delastr.is_good:
                        self.score_count.update_score()
                    else:
                        self.player.damaged()
                del delastr

        keys = pygame.key.get_pressed()
        if  keys[pygame.K_DOWN]:
            self.player.move("y")
        elif keys[pygame.K_UP]:
            self.player.move("-y")
        elif  keys[pygame.K_RIGHT]:
            self.player.move("x")
        elif keys[pygame.K_LEFT]:
            self.player.move("-x")
        if self.player.is_dead:
            self.is_end = True

    def main_loop(self):
        self.tick_count = 120
        while not self.is_end:
            self.event_handler()
            self.game_logic()
            self.render_engine.add_render_object(self.player,*self.asteroids)
            self.render_engine.render_frame(self.player.lives,self.score_count.score)
            self.clock.tick(consts.game_FPS)
            self.tick_count += 1
        pygame.quit()
