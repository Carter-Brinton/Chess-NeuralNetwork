import pygame
from constants.constants import *


class ChessRestartQuitUI:
    def __init__(self, chess_ui):
        self.chess_ui = chess_ui
        
    def draw_restart_game_button(self, ui_x_start, ui_y_start, ui_height):
        button_width = 110
        button_height = 30

        # Create restart button
        self.restart_button_rect = pygame.Rect(
            ui_x_start, ui_y_start + ui_height + 10, button_width, button_height
        )
        pygame.draw.rect(
            self.chess_ui.screen, pygame.Color("darkgrey"), self.restart_button_rect
        )
        font = pygame.font.Font(None, 22)
        text = font.render("Restart Game", True, BLACK)
        text_rect = text.get_rect(center=self.restart_button_rect.center)
        self.chess_ui.screen.blit(text, text_rect)

        # Create quit button
        self.quit_button_rect = pygame.Rect(
            ui_x_start + (button_width + 5),
            ui_y_start + ui_height + 10,
            button_width,
            button_height,
        )
        pygame.draw.rect(self.chess_ui.screen, pygame.Color("darkgrey"), self.quit_button_rect)
        text = font.render("Quit Game", True, BLACK)
        text_rect = text.get_rect(center=self.quit_button_rect.center)
        self.chess_ui.screen.blit(text, text_rect)
