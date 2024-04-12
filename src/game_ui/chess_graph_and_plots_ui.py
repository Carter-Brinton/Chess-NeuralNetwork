import pygame
from neural_network.neural_network import NeuralNetwork
import torch
from torchviz import make_dot
import matplotlib.pyplot as plt

class ChessGraphAndPlotsUI:
    def __init__(self, chess_ui):
        self.chess_ui = chess_ui

    def visualize_neural_network(self):
        # Create the model and input tensor
        model = NeuralNetwork(4096)
        x = torch.randn(1, 14, 8, 8)
        out = model(x)

        # Generate visualization
        dot = make_dot(out, params=dict(list(model.named_parameters()) + [('input', x)]))
        dot.format = 'png'
        dot.render('model_visualization')

        # Load and blit the rendered visualization
        nn_viz_image = pygame.image.load('model_visualization.png')
        self.chess_ui.screen.blit(nn_viz_image, (self.chess_ui.screen.get_width() - nn_viz_image.get_width(), 0))

    def plot_episode_rewards(self, episode_rewards_white, episode_rewards_black, episode_losses, epsilon_values):
        # Create plot
        plt.figure(figsize=(10, 5))
        plt.subplot(121)
        plt.plot(episode_rewards_white, label='White Reward')
        plt.plot(episode_rewards_black, label='Black Reward')
        plt.title('Rewards per Episode')
        plt.xlabel('Episode')
        plt.ylabel('Total Reward')
        plt.legend()

        plt.subplot(122)
        plt.plot(episode_losses, label='Loss')
        plt.plot(epsilon_values, label='Epsilon', secondary_y=True)
        plt.title('Loss and Epsilon Decay')
        plt.xlabel('Episode')
        plt.legend()
        
        # Save plot to file
        plt.savefig('training_progress.png')
        plt.close()

        # Load and blit the plot image
        plot_image = pygame.image.load('training_progress.png')
        self.chess_ui.screen.blit(plot_image, (self.chess_ui.screen.get_width() - plot_image.get_width(), 300))

    def update_graph_and_plots_ui(self, episode_rewards_white, episode_rewards_black, episode_losses, epsilon_values):
        # Call these functions whenever you want to update the graphs
        self.visualize_neural_network()
        self.plot_episode_rewards(episode_rewards_white, episode_rewards_black, episode_losses, epsilon_values)
        pygame.display.update() 
