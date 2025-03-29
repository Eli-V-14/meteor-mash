from settings import *
from pygame import Color
import pygame
import math

class Spaceship:
    def __init__(self, display):
        self.display = display
        self.img = pygame.image.load('images/spaceship1.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (91, 91))
        # self.img.set_colorkey(Color('blue'))
        # self.scaled_img = pygame.transform.scale(self.img, (100, 100))
        self.angle = 0
        self.x = WINDOW_HALF_WIDTH / 2 + self.img.get_width() / 2
        self.y = WINDOW_HALF_HEIGHT  + self.img.get_width() / 2

        self.cosine = 0
        self.sine = 0

        self.speed = 1
        self.acceleration = 2
        self.top = -self.img.get_height() / 2
        self.bottom = WINDOW_HEIGHT + self.img.get_height() / 2
        self.left = -self.img.get_width() / 2
        self.right = WINDOW_HALF_WIDTH + self.img.get_width() / 2
    
    def draw(self, img, rect):
        self.display.blit(img, rect)

    def update(self, events):

        keys = pygame.key.get_pressed()

        img = self.img

        if keys[pygame.K_RIGHT]:
            self.angle -= 0.55
        elif keys[pygame.K_LEFT]:
            self.angle += 0.55
        
        self.cosine = math.cos(math.radians((self.get_angle() % 360) + 90))
        self.sine = math.sin(math.radians((self.get_angle() % 360) - 90))
        
        if keys[pygame.K_w]:
            self.x += self.cosine * self.speed
            self.y += self.sine * self.speed
            img = pygame.image.load('images/spaceship2.png')
            img = pygame.transform.scale(img, (91, 91))
        else:
            img = self.img

        # x_dist = pos[0] - self.x
        # y_dist = -(pos[1] - self.y)
        # angle = math.degrees(math.atan2(y_dist, x_dist))

        if self.x > self.right:
            self.x = self.left
        elif self.x < self.left:
            self.x = self.right

        if self.y > self.bottom:
            self.y = self.top
        elif self.y < self.top:
            self.y = self.bottom

        rot_img = pygame.transform.rotate(img, self.angle)
        scaled_rect = self.img.get_rect(center = (self.x - rot_img.get_width() / 2, self.y - rot_img.get_height() / 2))

        self.draw(rot_img, scaled_rect)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
    
    def get_angle(self):
        return self.angle
    