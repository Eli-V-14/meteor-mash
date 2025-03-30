from settings import *
from spaceship import Spaceship
from pygame import Color
from bullet import Bullet
from asteroid import Asteroid
import pygame
import random

class Level:
    def __init__(self, display, gameStateManager, delta_time):
        pygame.init()
        self.display = display
        self.gameStateManager = gameStateManager
        self.delta_time = delta_time
        self.spaceship = Spaceship(self.display, delta_time)
        self.bullets = []
        self.asteroids = []
        self.count = 0
    
    def run(self, events):
        self.count += 1
        font = pygame.font.Font('fonts/sonic-advance-2-regular.ttf', int(WINDOW_HEIGHT * 0.025))
        text = font.render('Meteor Mash: Game', True, Color('white'))

        self.display.fill(Color('black'))
        self.display.blit(text, (0, 0))

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.gameStateManager.set_state('pause')
                elif event.key == pygame.K_SPACE:
                    self.bullets.append(Bullet(self.display, self.spaceship, self.delta_time))
        
        # print(self.count)

        if self.count % 500 == 0:
            rank = random.choice([1, 1, 1, 2, 2, 3])
            self.asteroids.append(Asteroid(self.display, rank, self.delta_time))
        
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     self.bullets.append(Bullet(self.display, self.spaceship))

        for a in self.asteroids:
            a.update()
            for b in self.bullets:
                b.update()

                if (a.x < b.x + b.width and a.x + a.width/2 > b.x and
                    a.y < b.y + b.height and a.y + a.height/2 > b.y):
                    if a.rank == 3:
                        n_a1 = Asteroid(self.display, 2, self.delta_time)
                        n_a1.x, n_a1.y = a.x, a.y
                        n_a2 = Asteroid(self.display, 2, self.delta_time)
                        n_a2.x, n_a2.y = a.x, a.y
                        self.asteroids.append(n_a1)
                        self.asteroids.append(n_a2)
                    elif a.rank == 2:
                        n_a1 = Asteroid(self.display, 1, self.delta_time)
                        n_a1.x, n_a1.y = a.x, a.y
                        n_a2 = Asteroid(self.display, 1, self.delta_time)
                        n_a2.x, n_a2.y = a.x, a.y
                        self.asteroids.append(n_a1)
                        self.asteroids.append(n_a2)
                    self.asteroids.remove(a)
                    self.bullets.remove(b)

                if not b.on_screen():
                    self.bullets.remove(b)
            if not a.on_screen():
                self.asteroids.remove(a)
                
                
            
            
        
        self.spaceship.update()
                
                

