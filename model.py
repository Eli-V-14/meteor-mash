import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

class DeepQNetwork(nn.Module):
    def __init__(self, lr, input_dims, fc1_dims, fc2_dims, n_actions):
        super(DeepQNetwork, self).__init__()
        self.input_dims = input_dims
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.n_actions = n_actions
        self.fc1 = nn.Linear(*self.input_dims, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)
        self.fc3 = nn.Linear(self.fc2_dims, self.n_actions)
        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.loss = nn.MSELoss()
        self.device = T.device('cuda')
        self.to(self.device)

    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        actions = self.fc3(x)

        return actions
    
class DQNAgent():
    def __init__(self, gamma, epsilon, lr, input_dims, batch_size, n_actions, 
                 max_mem_size=100000, eps_end=0.01, eps_dec=5e-4):
        self.gamma = gamma
        self.epsilon = epsilon
        self.lr = lr
        self.input_dims = input_dims
        self.batch_size = batch_size
        self.n_actions = n_actions
        self.max_mem_size = max_mem_size
        self.eps_end = eps_end
        self.eps_dec = eps_dec

        self.action_space = [i for i in range(n_actions)]
        self.mem_counter = 0
        
        self.Q_eval = DeepQNetwork(self.lr, n_actions=n_actions, input_dims=input_dims,
                                   fc1_dims=256, fc2_dims=256)
        
        self.Q_target = DeepQNetwork(self.lr, n_actions=n_actions, input_dims=input_dims,
                             fc1_dims=256, fc2_dims=256)
        self.Q_target.load_state_dict(self.Q_eval.state_dict())
        self.Q_target.eval()

        self.learn_step_counter = 0
        self.target_update_freq = 1000

        self.state_memory = np.zeros((self.max_mem_size, *input_dims), dtype=np.float32)
        self.new_state_memory = np.zeros((self.max_mem_size, *input_dims), dtype=np.float32)

        self.action_memory = np.zeros(self.max_mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.max_mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.max_mem_size, dtype=bool)

    def store_transitions(self, state, action, reward, state_, done):
        index = self.mem_counter % self.max_mem_size

        flattened_state = np.concatenate([
            np.array(state['spaceship_pos']).flatten(),
            np.array(state['spaceship_rot']).flatten(),
            np.array(state['rays']).flatten()
        ])

        flattened_state = self._normalize(flattened_state)

        # print(flattened_state)

        flattened_state_ = np.concatenate([
            np.array(state_['spaceship_pos']).flatten(),
            np.array(state_['spaceship_rot']).flatten(),
            np.array(state_['rays']).flatten()
        ])

        flattened_state_ = self._normalize(flattened_state_)

        self.state_memory[index] = flattened_state
        self.new_state_memory[index] = flattened_state_
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.terminal_memory[index] = done

        self.mem_counter += 1

    def choose_action(self, observation):
        if np.random.random() > self.epsilon:
            observation = np.concatenate([
                np.array(observation['spaceship_pos']).flatten(),
                np.array(observation['spaceship_rot']).flatten(),
                np.array(observation['rays']).flatten()
            ])
            state = T.tensor(observation, dtype=T.float32).to(self.Q_eval.device)
            actions = self.Q_eval.forward(state)
            action = T.argmax(actions).item()
        else:
            action = np.random.choice(self.action_space)
        return action
    
    def learn(self):
        if self.mem_counter < self.batch_size:
            return
        self.Q_eval.optimizer.zero_grad()

        max_mem = min(self.mem_counter, self.max_mem_size)
        batch = np.random.choice(max_mem, self.batch_size, replace=False)
        batch_index = np.arange(self.batch_size, dtype=np.int32)

        state_batch = T.tensor(self.state_memory[batch]).to(self.Q_eval.device)
        new_state_batch = T.tensor(self.new_state_memory[batch]).to(self.Q_eval.device)
        reward_batch = T.tensor(self.reward_memory[batch]).to(self.Q_eval.device)
        terminal_batch = T.tensor(self.terminal_memory[batch]).to(self.Q_eval.device)

        action_batch = self.action_memory[batch]

        q_eval = self.Q_eval.forward(state_batch)[batch_index, action_batch]

        q_next = self.Q_target.forward(new_state_batch)
        q_next[terminal_batch.bool()] = 0.0
        q_target = reward_batch + self.gamma * T.max(q_next, dim=1)[0]

        # loss = self.Q_eval.loss(q_eval, q_target.detach()).to(self.Q_eval.device)
        loss = F.smooth_l1_loss(q_eval, q_target.detach())
        loss.backward()
        self.Q_eval.optimizer.step()

        self.learn_step_counter += 1
        if self.learn_step_counter % self.target_update_freq == 0:
            self.Q_target.load_state_dict(self.Q_eval.state_dict())

        self.epsilon = self.epsilon - self.eps_dec if self.epsilon > self.eps_end else self.eps_end

    def _normalize(self, obs):
        pos = obs[0:2]
        rot = obs[2:3]

        ray_data = obs[3:].reshape(-1, 3)
        ray_data[:, 0] = ray_data[:, 0] / 2000.0 

        rays_normalized = ray_data.flatten()
        return np.concatenate([pos, rot, rays_normalized])
