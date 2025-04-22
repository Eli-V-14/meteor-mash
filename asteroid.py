from settings import *
from pygame import Color
import pygame
import random

class Asteroid:
    def __init__(self, display, rank):
        self.display = display
        self.rank = rank
        self.delta_time = 0

        if self.rank == 1:
            self.image = pygame.image.load('images/asteroid1.1.png')
        elif self.rank == 2:
            self.image = pygame.image.load('images/asteroid2.1.png')
        else:
            self.image = pygame.image.load('images/asteroid3.1.png')
        
        self.width = int(self.image.get_width())
        self.height = int(self.image.get_height())

        self.rand_point = random.choice([(random.randrange(0, int(WINDOW_HALF_WIDTH)  - self.width), random.choice([-1 * self.height - 5, int(WINDOW_HEIGHT) + 5])), 
                                         (random.choice([-1 * self.width - 5, int(WINDOW_HALF_WIDTH) + 5]), random.randrange(0, int(WINDOW_HEIGHT) - self.height))])
        
        self.x, self.y = self.rand_point
        # self.x, self.y = WINDOW_HALF_WIDTH / 2, WINDOW_HALF_HEIGHT

        self.xdir = 1 if self.x < WINDOW_HALF_WIDTH // 2 else -1
        self.ydir = 1 if self.y < WINDOW_HEIGHT // 2 else -1
        
        self.xv = self.xdir * random.randrange(1, 3) * 100
        self.yv = self.ydir * random.randrange(1, 3) * 100
        # self.xv = 0
        # self.yv = 0

    def move(self, delta_time):
        self.x += self.xv * delta_time
        self.y += self.yv * delta_time

    def draw(self, display):
        scaled_img = pygame.transform.scale(self.image, (self.width, self.height)).convert_alpha()
        
        display.blit(scaled_img, (self.x, self.y))

    def update(self, delta_time):
        self.move(delta_time)
        self.draw(self.display)
    
    def on_screen(self):
        return -250 < self.x < WINDOW_HALF_WIDTH + 250 and -250 < self.y < WINDOW_HEIGHT + 50
