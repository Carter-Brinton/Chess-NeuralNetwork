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
        self.memory = deque(maxlen=10000)  # Experience replay buffer
        self.gamma = 0.95  # Discount factor for future rewards
        self.epsilon = 1.0  # Exploration rate starts at 100%
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.epsilon_decay = 0.995  # Decay rate for exploration probability
        self.model = NeuralNetwork(action_size)  # The neural network model
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # Add experience to memory

    def act(self, state):
        if random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.FloatTensor(state).unsqueeze(0)  # Ensure proper tensor shape
        with torch.no_grad():
            action_values = self.model(state)
        return torch.argmax(action_values).item()

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return 0  # Return a zero loss if the memory is too small

        minibatch = random.sample(self.memory, batch_size)
        losses = []  # To store loss values for averaging

        for state, action, reward, next_state, done in minibatch:
            state = torch.FloatTensor(state)
            next_state = torch.FloatTensor(next_state)
            target = reward if done else reward + self.gamma * torch.max(self.model(next_state)).item()

            current_q_values = self.model(state)
            target_q_values = current_q_values.clone()
            target_q_values[0][action] = target

            self.optimizer.zero_grad()
            loss = F.mse_loss(current_q_values, target_q_values)
            loss.backward()
            self.optimizer.step()

            losses.append(loss.item())  # Store the loss value

        average_loss = sum(losses) / len(losses) if losses else 0  # Calculate average loss
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)  # Decay the epsilon value

        return average_loss  # Return the average loss