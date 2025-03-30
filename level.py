from settings import *
from spaceship import Spaceship
from pygame import Color
from bullet import Bullet
from asteroid import Asteroid
import pygame
import random

class Level:
    def __init__(self, display, gameStateManager):
        pygame.init()
        self.display = display
        self.gameStateManager = gameStateManager
        self.spaceship = Spaceship(self.display)
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
                    self.bullets.append(Bullet(self.display, self.spaceship))
        
        print(self.count)

        if self.count % 200 == 0:
            rank = random.choice([1, 1, 1, 2, 2, 3])
            self.asteroids.append(Asteroid(self.display, rank))
        
        # keys = pygame.key.get_pressed()

        # if keys[pygame.K_SPACE]:
        #     self.bullets.append(Bullet(self.display, self.spaceship))

        for asteroid in self.asteroids:
            asteroid.update()

        for bullet in self.bullets:
            bullet.update()
        
        # self.asteroids = [asteroid for asteroid in self.asteroids if asteroid.on_screen()]
        self.bullets = [bullet for bullet in self.bullets if bullet.on_screen()]
        
        self.spaceship.update(events)
                
                

