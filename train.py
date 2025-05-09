import gym
import numpy as np
import torch as T
import meteorMashEnv

from model import DQNAgent

env = gym.make('MeteorMash-v0')

gamma = 0.99
epsilon = 1.0
lr = 5e-4
input_dims = 219
print(input_dims)
batch_size = 64
n_actions = 5
max_mem_size = 100000
eps_end = 0.01
eps_dec = 0.000025

agent = DQNAgent(gamma=gamma, epsilon=epsilon, lr=lr, input_dims=(input_dims,), 
                 batch_size=batch_size, n_actions=n_actions, max_mem_size=max_mem_size,
                 eps_end=eps_end, eps_dec=eps_dec)

n_episodes = 500
max_steps = 1000
episode_rewards = []

for episode in range(n_episodes):
    state, info = env.reset()
    done = False
    total_reward = 0

    for step in range(max_steps):
        action = agent.choose_action(state)

        next_state, reward, terminated, truncated, info = env.step(action)

        env.render()
        
        total_reward += reward

        done = terminated or truncated

        agent.store_transitions(state, action, reward, next_state, done)

        if agent.mem_counter > 1000:
            agent.learn()

        state = next_state

        if terminated:
            break

    episode_rewards.append(total_reward)
    print(f"Episode {episode+1}/{n_episodes}, Total Reward: {total_reward}, Epsilon: {agent.epsilon:.4f}")

    if (episode + 1) % 100 == 0:
        T.save(agent.Q_eval.state_dict(), f"dqn_meteor_mash_{episode+1}.pth")
        print(f"dqn_meteor_mash_{episode+1}.pth")

env.close()