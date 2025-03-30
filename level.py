from settings import *
from spaceship import Spaceship
from pygame import Color
from bullet import Bullet
import pygame

class Level:
    def __init__(self, display, gameStateManager):
        pygame.init()
        self.display = display
        self.gameStateManager = gameStateManager
        self.spaceship = Spaceship(self.display)
        self.bullets = []
    
    def run(self, events):
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
                    
        
        # keys = pygame.key.get_pressed()

        # if keys[pygame.K_SPACE]:
        #     self.bullets.append(Bullet(self.display, self.spaceship))
        
        for bullet in self.bullets:
            bullet.update()

        self.bullets = [bullet for bullet in self.bullets if not bullet.off_screen()]
        
        self.spaceship.update(events)
                
                

