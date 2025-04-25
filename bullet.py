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

        self.cosine = spaceship.cosine
        self.sine = spaceship.sine
        self.xv = self.cosine * 750
        self.yv = -self.sine * 750

        self.count = 0
    
    def move(self, delta_time):
        self.x += self.xv * delta_time
        self.y -= self.yv * delta_time
    
    def draw(self, display):        
        pygame.draw.rect(display, Color('royalblue1'), [self.x - self.img_width - self.width / 4, self.y - self.img_height, self.width, self.height])
    
    def update(self, delta_time):
        self.move(delta_time)
        self.draw(self.display)
    
    def on_screen(self):
        return 0 + self.img_width < self.x < WINDOW_HALF_WIDTH + self.img_width and 0 + self.img_height < self.y < WINDOW_HEIGHT + self.img_height