import gym
from gym import spaces
import numpy as np
import pygame
from main import Game

class AsteroidEnv(gym.Env):
    def __init__(self):
        super(AsteroidEnv, self).__init__()
        self.game = Game()