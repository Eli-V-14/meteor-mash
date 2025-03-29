from settings import *
from pygame import Color
import pygame
import math

class Spaceship:
    def __init__(self, display):
        self.display = display
        self.img = pygame.image.load('images/spaceship1.png').convert_alpha()
        # self.img.set_colorkey(Color('blue'))
        # self.scaled_img = pygame.transform.scale(self.img, (100, 100))
        self.angle = 0
        self.x = WINDOWN_HALF_WIDTH / 2 + self.img.get_width() / 2
        self.y = WINDOW_HALF_HEIGHT  + self.img.get_width() / 2
        self.speed = 1.5
        self.acceleration = 2
    
    def draw(self, img, rect):
        self.display.blit(img, rect)

    def update(self, events):
        pos = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed()

        img = self.img

        if keys[pygame.K_RIGHT]:
            self.angle -= 0.55
        elif keys[pygame.K_LEFT]:
            self.angle += 0.55
        
        if keys[pygame.K_w]:
            self.x += math.cos(math.radians((self.angle % 360) + 90)) * self.speed
            self.y += math.sin(math.radians((self.angle % 360) - 90)) * self.speed
            img = pygame.image.load('images/spaceship2.png')
        else:
            img = self.img

        # x_dist = pos[0] - self.x
        # y_dist = -(pos[1] - self.y)
        # angle = math.degrees(math.atan2(y_dist, x_dist))

        scaled_img = pygame.transform.scale(img, (91, 91))
        rot_img = pygame.transform.rotate(scaled_img, self.angle)
        scaled_rect = self.img.get_rect(center = (self.x - rot_img.get_width() / 2, self.y - rot_img.get_height() / 2))

        self.draw(rot_img, scaled_rect)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
    