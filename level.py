from settings import *
from pygame import Color
from spaceship import Spaceship
import pygame

class Level:
    def __init__(self, display, gameStateManager):
        pygame.init()
        self.display = display
        self.gameStateManager = gameStateManager
        self.spaceship = Spaceship(self.display)
    
    def run(self, events):
        font = pygame.font.Font('fonts/sonic-advance-2-regular.ttf', int(WINDOW_HEIGHT * 0.025))
        text = font.render('Meteor Mash: Game', True, Color('white'))

        self.display.fill(Color('black'))
        self.display.blit(text, (0, 0))

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.gameStateManager.set_state('pause')
        
        self.spaceship.update(events)
                
                

