from settings import *
from pygame import Color
from bullet import Bullet
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
        self.y = WINDOW_HALF_HEIGHT  + self.img.get_height() / 2
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.cosine = 0
        self.sine = 0
        self.delta_time = 0

        self.top = -self.img.get_height() / 2
        self.bottom = WINDOW_HEIGHT + self.img.get_height() / 2
        self.left = -self.img.get_width() / 2
        self.right = WINDOW_HALF_WIDTH + self.img.get_width() / 2
    
    def draw(self, img, rect):
        self.display.blit(img, rect)

    def update(self, delta_time):
        self.set_delta_time(delta_time)

        keys = pygame.key.get_pressed()

        img = self.img

        # COMMENTED OUT FOR THE USE OF THE DEEP Q-LEARNING NETWORK
        # if keys[pygame.K_RIGHT]:
        #     self.move_right()
        # elif keys[pygame.K_LEFT]:
        #     self.move_left()
        
        self.cosine = math.cos(math.radians((self.get_angle()) + 90))
        self.sine = math.sin(math.radians((self.get_angle()) - 90))
        
        if keys[pygame.K_w]:
            # COMMENTED OUT FOR THE USE OF THE DEEP Q-LEARNING NETWORK
            # self.move_forward()
            img = pygame.image.load('images/spaceship2.png')
            img = pygame.transform.scale(img, (91, 91))
        else:
            img = self.img

        self.check_borders()

        # COMMENTED OUT FOR THE USE OF KEYBOARD INPUTS INSTEAD OF MOUSE LOCATION
        # x_dist = pos[0] - self.x
        # y_dist = -(pos[1] - self.y)
        # angle = math.degrees(math.atan2(y_dist, x_dist))

        rot_img = pygame.transform.rotate(img, self.get_angle())
        scaled_rect = self.img.get_rect(center = (self.x - rot_img.get_width() / 2, self.y - rot_img.get_height() / 2))

        self.draw(rot_img, scaled_rect)
    
    def get_angle(self):
        return self.angle
    
    def set_delta_time(self, delta_time):
        self.delta_time = delta_time
    
    def get_delta_time(self):
        return self.delta_time
    
    def check_borders(self):
        if self.x > self.right:
            self.x = self.left
        elif self.x < self.left:
            self.x = self.right

        if self.y > self.bottom:
            self.y = self.top
        elif self.y < self.top:
            self.y = self.bottom

    def move_forward(self):
        self.x += self.cosine * 250 * self.get_delta_time()
        self.y += self.sine * 250 * self.get_delta_time()
    
    def move_right(self):
        self.angle -= 5

    def move_left(self):
        self.angle += 5
    
    def shoot(self):
        return Bullet(self.display, self)
    