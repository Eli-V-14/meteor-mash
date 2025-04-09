from settings import *
from spaceship import Spaceship
from pygame import Color
from bullet import Bullet
from asteroid import Asteroid
import pygame
import random

class Level:
    def __init__(self, display, gameStateManager):
        pygame.init()
        self.display = display
        self.gameStateManager = gameStateManager
        self.spaceship = Spaceship(self.display)
        self.bullets = []
        self.asteroids = []
        self.count = 0
        self.score = 0

        self.last_bullet_frame = 0
        self.total_frames = 0

    def shoot(self):
        self.bullets.append(self.spaceship.shoot())
    
    def run(self, events, delta_time):
        self.count += 1

        delta_time = delta_time if delta_time < 0.01 else 0.016
        self.render_text()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.gameStateManager.set_state('pause')
                elif event.key == pygame.K_SPACE:
                    self.shoot()

        if self.count % 75 == 0:
            self.generate_asteroids()

        # Spamming Shoot Button        
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     self.bullets.append(Bullet(self.display, self.spaceship))

        for b in self.bullets:   
            b.update(delta_time)

        for a in self.asteroids:
            a.update(delta_time)
        
        self.check_collisions(delta_time)
                
        self.spaceship.update(delta_time)
    
    def render_text(self):
        font = pygame.font.Font('fonts/sonic-advance-2-regular.ttf', int(WINDOW_HEIGHT * 0.025))
        text = font.render('Meteor Mash: Game', True, Color('white'))

        score = 'Score: ' + str(self.score)
        score_text = font.render(score, True, Color('white'))

        self.display.fill(Color('black'))
        self.display.blit(text, (0, 0))
        self.display.blit(score_text, (0, int(WINDOW_HEIGHT * 0.025)))

    def generate_asteroids(self):
        rank = random.choice([1, 1, 1, 2, 2, 3])
        self.asteroids.append(Asteroid(self.display, rank))

    def split_asteroids(self, asteroid, rank):
        n_a1 = Asteroid(self.display, rank - 1)
        n_a1.x, n_a1.y = asteroid.x, asteroid.y
        n_a2 = Asteroid(self.display, rank - 1)
        n_a2.x, n_a2.y = asteroid.x, asteroid.y
        self.asteroids.append(n_a1)
        self.asteroids.append(n_a2)
    
    def check_collisions(self, delta_time):
        spaceship_rect = pygame.Rect(self.spaceship.x - self.spaceship.width, self.spaceship.y - self.spaceship.height, 
                                     self.spaceship.width, self.spaceship.height)
        pygame.draw.rect(self.display, Color('green'), spaceship_rect, 2)

        for a in self.asteroids:
            asteroid_rect = pygame.Rect(a.x, a.y, a.width, a.height)
            pygame.draw.rect(self.display, Color('red'), asteroid_rect, 2)

            if spaceship_rect.colliderect(asteroid_rect):
                self.gameStateManager.set_state('lost')

            for b in self.bullets:
                bullet_rect = pygame.Rect(b.x - b.img_width - b.width / 4, b.y - b.img_height, b.width, b.height)
                pygame.draw.rect(self.display, Color('blue'), bullet_rect, 2)

                if asteroid_rect.colliderect(bullet_rect):
                    if a.rank == 3:
                        self.split_asteroids(a, a.rank)
                    self.score += 50 * a.rank
                    self.asteroids.remove(a)
                    self.bullets.remove(b)

                if not b.on_screen():
                    self.bullets.remove(b)
            if not a.on_screen():
                self.asteroids.remove(a)

    def restart(self):
        self.gameStateManager = self.gameStateManager
        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship(self.display)
        self.count = 0
        self.score = 0

        observation = self._get_obs()
        info = self._get_info()

        return observation, info