import gym
from meteorMashEnv import MeteorMashEnv

env = MeteorMashEnv()

obs, info = env.reset()

for _ in range(5000):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

    env.render()

    if terminated:
        break

env.close()