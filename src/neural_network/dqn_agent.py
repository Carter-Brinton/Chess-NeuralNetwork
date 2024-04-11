# dqn_agent.py
import torch
import torch.optim as optim
import torch.nn.functional as F
import random
from collections import deque
from neural_network.neural_network import NeuralNetwork

class DQNAgent:
    def __init__(self, state_size, action_size, lr=1e-4):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.gamma = 0.95  # discount factor
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = NeuralNetwork(self.action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            action_values = self.model(state)
        return torch.argmax(action_values).item()

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_state = torch.FloatTensor(next_state).unsqueeze(0)
                target = (reward + self.gamma * torch.max(self.model(next_state)).item())
            state = torch.FloatTensor(state).unsqueeze(0)
            target_f = self.model(state)
            target_f[0][action] = target
            self.optimizer.zero_grad()
            loss = F.mse_loss(target_f, target_f)
            loss.backward()
            self.optimizer.step()
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
