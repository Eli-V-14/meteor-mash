from settings import *
from pygame import Color
import pygame
import random

class Asteroid:
    def __init__(self, display, rank, delta_time):
        self.display = display
        self.rank = rank
        self.delta_time = delta_time

        if self.rank == 1:
            self.image = pygame.image.load('images/asteroid1.png')
        elif self.rank == 2:
            self.image = pygame.image.load('images/asteroid2.png')
        else:
            self.image = pygame.image.load('images/asteroid3.png')
        
        self.width = int(self.image.get_width() * 1.25)
        self.height = int(self.image.get_height() * 1.25)

        self.rand_point = random.choice([(random.randrange(0, int(WINDOW_HALF_WIDTH)  - self.width), random.choice([-1 * self.height - 5, int(WINDOW_HEIGHT) + 5])), 
                                         (random.choice([-1 * self.width - 5, int(WINDOW_HALF_WIDTH) + 5]), random.randrange(0, int(WINDOW_HEIGHT) - self.height))])
        
        self.x, self.y = self.rand_point

        self.xdir = 1 if self.x < WINDOW_HALF_WIDTH // 2 else -1
        self.ydir = 1 if self.y < WINDOW_HEIGHT // 2 else -1
        
        self.xv = self.xdir * delta_time * random.randrange(3, 5)
        self.yv = self.ydir * delta_time * random.randrange(3, 5)

    def move(self):
        self.x += self.xv
        self.y += self.yv

    def draw(self, display):
        # scaled_img = pygame.transform.scale(self.image, (self.width, self.height)).convert_alpha()
        # scaled_img.set_colorkey(Color('blue'))
        
        # display.blit(scaled_img, (self.x, self.y))

        
        # Create a surface for the background with the desired color
        background_surface = pygame.Surface((self.width, self.height))
        background_surface.fill(Color('gray'))  # Change 'gray' to any color you want

        # Scale and set transparency for the asteroid image
        scaled_img = pygame.transform.scale(self.image, (self.width, self.height)).convert_alpha()
        scaled_img.set_colorkey(Color('blue'))  # Assuming 'blue' is used as the transparency key
        
        # Blit the background color surface first
        display.blit(background_surface, (self.x, self.y))
        
        # Now, blit the asteroid image on top
        display.blit(scaled_img, (self.x, self.y))

    def update(self):
        self.move()
        self.draw(self.display)
    
    def on_screen(self):
        return -250 < self.x < WINDOW_HALF_WIDTH + 250 and -250 < self.y < WINDOW_HEIGHT + 50
