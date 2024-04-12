import pygame
from constants.constants import *
from neural_network.neural_network import NeuralNetwork
import torch
from torchviz import make_dot
import matplotlib.pyplot as plt

class ChessTrainingStatsUI:
    def __init__(self, chess_ui):
        self.chess_ui = chess_ui

    def draw_training_stats(self):
        # Popup dimensions and position
        popup_width = 30
        popup_height = 20
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2

        # Popup background
        pygame.draw.rect(
            self.chess_ui.screen, RED, (popup_x, popup_y, popup_width, popup_height)
        )

        # label_font = pygame.font.Font(None, 24)
        # move_text_font = pygame.font.Font(None, 30) 
        # player_color = 'BLACK'
        # move_text = f"Player '{player_color}' to Move"
        # move_text_surface = move_text_font.render(move_text, True, BLACK)

        # # Calculate the position to center the text above the board
        # text_x = OFFSET_X + (BOARD_SIZE - move_text_surface.get_width()) // 2
        # text_y = OFFSET_Y - move_text_surface.get_height() - 15  # 20 pixels above the board
        # self.chess_ui.screen.blit(move_text_surface, (text_x, text_y))
    
        # font = pygame.font.Font(None, 20)
        # move_text = "TEMP"
        # # move_text = f"Number of Episodes: '{episode}', White Score: '{total_reward_white}', Black Score: '{total_reward_black}', Loss: '{episode_loss}','"
        # move_text_surface = font.render(move_text, True, BLACK)

        # # Calculate the position to center the text above the board
        # text_x = OFFSET_X + (BOARD_SIZE - move_text_surface.get_width()) // 2
        # text_y = OFFSET_Y - move_text_surface.get_height() - 20  # 20 pixels above the board
        # self.chess_ui.screen.blit(move_text_surface, (text_x, text_y))