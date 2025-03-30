from settings import *
import pygame
import random

class Asteroid:
    def __init__(self, display, rank):
        self.display = display
        self.rank = rank
        if self.rank == 1:
            self.image = pygame.image.load('images/asteroid1.png')
        elif self.rank == 2:
            self.image = pygame.image.load('images/asteroid2.png')
        else:
            self.image = pygame.image.load('images/asteroid3.png')
        
        self.width = 50 * rank
        self.height = 50 * rank

        self.rand_point = random.choice([(random.randrange(0, int(WINDOW_HALF_WIDTH)  - self.width), random.choice([-1 * self.height - 5, int(WINDOW_HEIGHT) + 5])), 
                                         (random.choice([-1 * self.width - 5, int(WINDOW_HALF_WIDTH) + 5]), random.randrange(0, int(WINDOW_HEIGHT) - self.height))])
        
        self.x, self.y = self.rand_point

        self.xdir = 1 if self.x < WINDOW_HALF_WIDTH // 2 else -1
        self.ydir = 1 if self.y < WINDOW_HEIGHT // 2 else -1
        
        self.xv = self.xdir * random.randrange(1, 2)
        self.yv = self.ydir * random.randrange(1, 2)

    def move(self):
        self.x += self.xv
        self.y += self.yv

    def draw(self, display):
        display.blit(self.image, (self.x, self.y))

    def update(self):
        self.move()
        self.draw(self.display)
    
    # def on_screen(self):
    #     return 0 < self.x < WINDOW_HALF_WIDTH and 0 < self.y < WINDOW_HEIGHT
