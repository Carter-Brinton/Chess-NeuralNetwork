import chess
import pygame
from constants.constants import *


class ChessStartGameUI:
    def __init__(self, chess_ui):
        self.chess_ui = chess_ui
        
    def draw_start_game_popup(self):
        self.chess_ui.draw_overlay()

        # Popup dimensions and position
        popup_width = 300
        popup_height = 290
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2

        # Popup background
        pygame.draw.rect(
            self.chess_ui.screen, GREY, (popup_x, popup_y, popup_width, popup_height)
        )

        # Draw buttons for selecting options
        font = pygame.font.Font(None, 36)
        start_train_button_rect = pygame.Rect(popup_x + 50, popup_y + 50, 200, 50)
        start_ai_button_rect = pygame.Rect(popup_x + 50, popup_y + 120, 200, 50)
        start_two_player_button_rect = pygame.Rect(popup_x + 50, popup_y + 190, 200, 50)

        pygame.draw.rect(self.chess_ui.screen, PALERED, start_train_button_rect)
        pygame.draw.rect(self.chess_ui.screen, PALEGREEN, start_ai_button_rect)
        pygame.draw.rect(self.chess_ui.screen, PALEBLUE, start_two_player_button_rect)
        pygame.draw.rect(self.chess_ui.screen, BLACK, start_train_button_rect, 1)  
        pygame.draw.rect(self.chess_ui.screen, BLACK, start_ai_button_rect, 1) 
        pygame.draw.rect(self.chess_ui.screen, BLACK, start_two_player_button_rect, 1)

        # Render text surfaces
        train_text = font.render("Train AI", True, BLACK)
        ai_text = font.render("Play against AI", True, BLACK)
        two_player_text = font.render("Player vs Player", True, BLACK)

        # Calculate text position for center alignment
        def center_text(rect, text_surface):
            return (
                rect.x + (rect.width - text_surface.get_width()) // 2,
                rect.y + (rect.height - text_surface.get_height()) // 2,
            )

        # Blit text surfaces at calculated positions
        self.chess_ui.screen.blit(train_text, center_text(start_train_button_rect, train_text))
        self.chess_ui.screen.blit(ai_text, center_text(start_ai_button_rect, ai_text))
        self.chess_ui.screen.blit(
            two_player_text, center_text(start_two_player_button_rect, two_player_text)
        )

        # Store rectangles for click detection
        self.start_train_button_rect = start_train_button_rect
        self.start_ai_button_rect = start_ai_button_rect
        self.start_two_player_button_rect = start_two_player_button_rect
