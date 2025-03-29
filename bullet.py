from settings import *
from pygame import Color
import pygame
import math

class Bullet:
    def __init__(self, display, spaceship):
        self.display = display
        self.x, self.y = spaceship.x, spaceship.y
        self.img_width = spaceship.img.get_width() / 2
        self.img_height = spaceship.img.get_height() / 2
        self.width = 6
        self.height = 6
        self.angle = spaceship.angle
        self.cosine = spaceship.cosine
        self.sine = spaceship.sine
        self.xv = self.cosine * 2.5
        self.yv = -self.sine * 2.5
    
    def move(self):
        self.x += self.xv
        self.y -= self.yv
    
    def draw(self, display):
        pygame.draw.rect(display, Color('royalblue1'), [self.x - self.img_width, self.y - self.img_height, self.width, self.height])
    
    def update(self):
        print(0, WINDOW_HALF_WIDTH)
        print(0, WINDOW_HALF_HEIGHT)
        print(self.x, self.y)
        self.move()
        self.draw(self.display)
    
    def off_screen(self):
        return self.x < 0 or self.x > WINDOW_HALF_WIDTH or self.y < 0 or self.y > WINDOW_HEIGHT