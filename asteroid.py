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
            self.image = pygame.image.load('image/asteroid3.png')
        
        self.width = 50 * rank
        self.height = 50 * rank

        self.rand_point = random.choice([(random.randrange(WINDOW_HALF_WIDTH - self.width), -self.height),
                                         (random.randrange(WINDOW_HALF_WIDTH - self.width), WINDOW_HEIGHT),
                                         (-self.width, random.randrange(WINDOW_HEIGHT - self.height)),
                                         (WINDOW_HALF_WIDTH, random.randrange(WINDOW_HEIGHT - self.height))])
        
        self.x, self.y = self.rand_point

        self.xdir = 1 if self.x < WINDOW_HALF_WIDTH // 2 else -1
        self.ydir = 1 if self.y < WINDOW_HEIGHT // 2 else -1
        
        self.xv = self.xdir * random.randrange(3, 6)
        self.yv = self.ydir * random.randrange(3, 6)

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
