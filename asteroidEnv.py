import gym
from gym import spaces
import numpy as np
import pygame
from dqn_main import Game

class AsteroidEnv(gym.Env):
    def __init__(self):
        super(AsteroidEnv, self).__init__()
        self.game = Game()

        self.action_space = spaces.Discrete(5)

        self.observation_space = spaces.Dict({
            "spaceship_pos": spaces.Box(low=0, high=1, shape=(2,), dtype=np.float32),
            "spaceship_rot": spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32),
            "asteroids": spaces.Box(low=-np.inf, high=np.inf, shape=(10, 5), dtype=np.float32),
            "bullets": spaces.Box(low=-np.inf, high=np.inf, shape=(10, 4), dtype=np.float32)
        })
    
    def reset(self):
        obs, info = self.game.level.restart()
        return obs, info
    
    def step(self, action):
        observation, reward, terminated, truncated, info = self.game.level.step(action)
        return observation, reward, terminated, truncated, info
    