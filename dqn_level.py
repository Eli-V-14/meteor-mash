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

        self.reward = 0

        self.terminated = bool(False)

    def step(self, action):
        """
        Maps the action taken by the agent to the spaceship's actions
        Utilized for Deep Q-Network Learning
        0 - Move Left
        1 - Move Right
        2 - Thrust
        3 - Fire
        4 - Do Nothing
        """
        self.total_frames += 1

        match action:
            case 0: 
                self.spaceship.move_left()
                # self.reward += 0.005
            case 1: 
                self.spaceship.move_right()
                # self.reward += 0.005
            case 2: 
                self.spaceship.move_forward()
                self.reward += 0.3
            case 3: 
                if (self.total_frames - self.last_bullet_frame) > 25:
                    self.shoot()
                    self.last_bullet_frame = self.total_frames
            case 4:
                pass
            case _:
                print(f"Invalid action: {action}")

        terminated = bool(self.terminated)
        truncated = False
        reward = self.get_rewards()
        observation = self._get_obs()
        info = self._get_info()        

        return observation, reward, bool(terminated), truncated, info

    def shoot(self):
        self.bullets.append(self.spaceship.shoot())
    
    def get_rewards(self):
        reward = 0  
        reward += self.reward
        self.reward = 0  

        return reward

    def _get_obs(self):        
        return {
            'spaceship_pos': [self.spaceship.x / WINDOW_HALF_WIDTH, self.spaceship.y / WINDOW_HEIGHT],
            'spaceship_rot': [(self.spaceship.angle % 360) / 360],
            'rays': self.spaceship.raycast(self.asteroids, 72, 300, 360)
        }

    def _get_info(self):
        asteroid_sizes = [[a.width, a.height] for a in self.asteroids]

        return {'remaining_asteroids':len(self.asteroids),
                'asteroid_sizes': asteroid_sizes}
    
    def run(self, events, delta_time):
        self.count += 1

        delta_time = delta_time if delta_time > 0.01 else 0.014
        self.render_text()

        if self.count % 50 == 0:
            self.generate_asteroids()

        for a in self.asteroids:
            a.update(delta_time)
        
        for b in self.bullets:   
            b.update(delta_time)

        self.check_collisions(delta_time)

        self.spaceship.raycast(self.asteroids, 72, 300, 360)

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
        # print('asteroid')
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
        # pygame.draw.rect(self.display, Color('green'), spaceship_rect, 2)

        self.terminated = self.spaceship.check_borders()
        if self.terminated:
            self.reward -= 50

        for a in self.asteroids:
            asteroid_rect = pygame.Rect(a.x, a.y, a.width, a.height)
            # pygame.draw.rect(self.display, Color('red'), asteroid_rect, 2)

            if spaceship_rect.colliderect(asteroid_rect):
                self.terminated = bool(True)
                # self.gameStateManager.set_state('lost')

            for b in self.bullets:
                bullet_rect = pygame.Rect(b.x - b.img_width - b.width / 4, b.y - b.img_height, b.width, b.height)
                # pygame.draw.rect(self.display, Color('blue'), bullet_rect, 2)

                if asteroid_rect.colliderect(bullet_rect):
                    if a.rank > 1:
                        self.split_asteroids(a, a.rank)
                        self.score += 50 * a.rank
                        self.reward += 2.5 * a.rank

                    self.score += 50
                    self.reward += 2.5
                    self.asteroids.remove(a)
                    self.bullets.remove(b)

                if not b.on_screen():
                    if b in self.bullets:
                        self.reward -= 2
                        self.bullets.remove(b)
            if not a.on_screen():
                if a in self.asteroids:
                    self.asteroids.remove(a)

    def restart(self):
        self.gameStateManager = self.gameStateManager
        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship(self.display)
        self.count = 0
        self.score = 0
        self.terminated = bool(False)

        return self._get_obs(), self._get_info()