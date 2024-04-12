# neural_network.py
import torch
import torch.nn as nn
import torch.nn.functional as F

class NeuralNetwork(nn.Module):
    def __init__(self, action_size):
        super(NeuralNetwork, self).__init__()
        # Adjust the number of input channels to match your board representation
        self.conv1 = nn.Conv2d(14, 16, kernel_size=3, stride=1, padding=1)
        # The rest of your network definition remains the same
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(32 * 8 * 8, 128)  # This might need adjustment based on the output of your conv layers
        self.fc2 = nn.Linear(128, 64)
        self.out = nn.Linear(64, action_size)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(x.size(0), -1)  # Flatten
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.out(x)
        return x
