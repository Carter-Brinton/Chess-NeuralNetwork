import chess
import pygame
from constants.constants import *


class ChessSelectColorUI:
    def __init__(self, chess_ui):
        self.chess_ui = chess_ui
        
    def draw_select_starting_color_ui(self):
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
        font = pygame.font.Font(None, 30)
        white_button_rect = pygame.Rect(popup_x + 50, popup_y + 50, 200, 50)
        black_button_rect = pygame.Rect(popup_x + 50, popup_y + 120, 200, 50)
        random_button_rect = pygame.Rect(popup_x + 50, popup_y + 190, 200, 50)

        pygame.draw.rect(self.chess_ui.screen, WHITE, white_button_rect)
        pygame.draw.rect(self.chess_ui.screen, BLACK, black_button_rect)
        self.chess_ui.draw_gradient_left_to_right(random_button_rect, WHITE, BLACK)

        # Render text surfaces
        white_text = font.render("Play as White", True, BLACK)
        black_text = font.render("Play as Black", True, WHITE)
        # random_text = font.render('Random Color', True, BLACK)
        self.chess_ui.draw_gradient_text("Random Color", font, random_button_rect, BLACK, WHITE)

        # Calculate text position for center alignment
        def center_text(rect, text_surface):
            return (
                rect.x + (rect.width - text_surface.get_width()) // 2,
                rect.y + (rect.height - text_surface.get_height()) // 2,
            )

        # Blit text surfaces at calculated positions
        self.chess_ui.screen.blit(white_text, center_text(white_button_rect, white_text))
        self.chess_ui.screen.blit(black_text, center_text(black_button_rect, black_text))
        # self.screen.blit(random_text, center_text(random_button_rect, random_text))

        # Store rectangles for click detection
        self.white_button_rect = white_button_rect
        self.black_button_rect = black_button_rect
        self.random_button_rect = random_button_rect