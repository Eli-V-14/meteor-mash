from settings import *
from pygame import Color
from bullet import Bullet
import pygame
import math
import random

class Spaceship:
    def __init__(self, display):
        self.display = display

        self.img = pygame.image.load('images/spaceship1.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (91, 91))
        # self.img.set_colorkey(Color('blue'))
        # self.scaled_img = pygame.transform.scale(self.img, (100, 100))

        self.angle = random.randrange(0, 360)
        self.x = WINDOW_HALF_WIDTH / 2 + self.img.get_width() / 2
        self.y = WINDOW_HALF_HEIGHT  + self.img.get_height() / 2
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.cosine = 0
        self.sine = 0
        self.delta_time = 0

        self.top = self.img.get_height()
        self.bottom = WINDOW_HEIGHT
        self.left = self.img.get_width()
        self.right = WINDOW_HALF_WIDTH
    
    def draw(self, img, rect):
        self.display.blit(img, rect)

    def update(self, delta_time):
        self.set_delta_time(delta_time)

        keys = pygame.key.get_pressed()

        img = self.img

        # COMMENTED OUT FOR THE USE OF THE DEEP Q-LEARNING NETWORK
        if keys[pygame.K_RIGHT]:
            self.move_right()
        elif keys[pygame.K_LEFT]:
            self.move_left()
        
        self.cosine = math.cos(math.radians((self.get_angle()) + 90))
        self.sine = math.sin(math.radians((self.get_angle()) - 90))
        
        if keys[pygame.K_w]:
            # COMMENTED OUT FOR THE USE OF THE DEEP Q-LEARNING NETWORK
            self.move_forward()
            img = pygame.image.load('images/spaceship2.png')
            img = pygame.transform.scale(img, (91, 91))
        else:
            img = self.img

        # COMMENTED OUT FOR THE USE OF KEYBOARD INPUTS INSTEAD OF MOUSE LOCATION
        # x_dist = pos[0] - self.x
        # y_dist = -(pos[1] - self.y)
        # angle = math.degrees(math.atan2(y_dist, x_dist))

        rot_img = pygame.transform.rotate(img, self.get_angle())
        centered_x = self.x - rot_img.get_width() / 2
        centered_y = self.y - rot_img.get_height() / 2
        scaled_rect = self.img.get_rect(center = (centered_x, centered_y))

        self.draw(rot_img, scaled_rect)
    
    def get_angle(self):
        return self.angle
    
    def set_delta_time(self, delta_time):
        self.delta_time = delta_time
    
    def get_delta_time(self):
        return self.delta_time
    
    def check_borders(self):
        if self.x > self.right or self.x < self.left or self.y > self.bottom or self.y < self.top:
            return True
        return False
    
    def move_forward(self):
        self.x += self.cosine * 350 * self.get_delta_time()
        self.y += self.sine * 350 * self.get_delta_time()
    
    def move_right(self):
        self.angle -= 5

    def move_left(self):
        self.angle += 5
    
    def shoot(self):
        return Bullet(self.display, self)
    
    def raycast(self, asteroids, ray_count, ray_length, cone_angle=90):
        ray_distances = []
        centered_x = self.x - self.width / 2
        centered_y = self.y - self.height / 2

        
        angle_start = self.angle + 90 - (cone_angle / 2)
        angle_step = cone_angle / (ray_count - 1)

        for i in range(ray_count):
            ray_angle = math.radians(angle_start + i * angle_step)
            dx = math.cos(-ray_angle)
            dy = math.sin(-ray_angle)

            distance = 0
            hit = False

            start_x = centered_x + dx * 50
            start_y = centered_y + dy * 50

            while distance < ray_length:
                test_x = start_x + dx * distance
                test_y = start_y + dy * distance

                # Check collision
                for a in asteroids:
                    a_rect = pygame.Rect(a.x, a.y, a.width, a.height)
                    if a_rect.collidepoint(test_x, test_y):
                        hit = True
                        break

                pygame.draw.circle(self.display, Color('gray5'), (int(test_x), int(test_y)), 2)

                if hit:
                    break

                distance += 5

            ray_distances.append((distance, math.cos(ray_angle), math.sin(ray_angle)))
        
        return ray_distances
    