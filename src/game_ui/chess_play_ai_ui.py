import chess
import pygame
from constants.constants import *


class ChessPlayAIUI:
    def __init__(self, chess_ui):
        self.chess_ui = chess_ui
        self.ai_levels = ["1 (Easy)", "2 (Less Easy)", "3 (Medium)", "4 (Less Hard)", "5 (Hard)"]
        self.current_level_index = 0  # Start with the first level, "Easy"
        self.ai_level_dropdown_rect = None
        self.ai_level_dropdown_selected_index = 0

    def draw_play_ai_popup(self):
        self.chess_ui.draw_overlay()

        # Popup dimensions and position
        popup_width = 300
        popup_height = 325  # Increase the height to accommodate the dropdown
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2
        font = pygame.font.Font(None, 30)
        # Popup background
        pygame.draw.rect(
            self.chess_ui.screen, GREY, (popup_x, popup_y, popup_width, popup_height)
        )

        if self.ai_level_dropdown_rect is None:
            self.ai_level_dropdown_rect = pygame.Rect(popup_x + 50, popup_y + 35, 200, 30)

        # Draw dropdown for selecting AI levels
        pygame.draw.rect(self.chess_ui.screen, WHITE, self.ai_level_dropdown_rect, 2)
        selected_level_text = self.ai_levels[self.ai_level_dropdown_selected_index]
        selected_level_surface = font.render(selected_level_text, True, BLACK)
        self.chess_ui.screen.blit(selected_level_surface, (self.ai_level_dropdown_rect.x + 5, self.ai_level_dropdown_rect.y + 5))

        # Draw buttons for selecting options
        white_button_rect = pygame.Rect(popup_x + 50, popup_y + 90, 200, 50)
        black_button_rect = pygame.Rect(popup_x + 50, popup_y + 160, 200, 50)
        random_button_rect = pygame.Rect(popup_x + 50, popup_y + 230, 200, 50)

        pygame.draw.rect(self.chess_ui.screen, WHITE, white_button_rect)
        pygame.draw.rect(self.chess_ui.screen, BLACK, black_button_rect)
        self.chess_ui.draw_gradient_left_to_right(random_button_rect, WHITE, BLACK)

        # Render text surfaces for buttons
        white_text = font.render("Play as White", True, BLACK)
        black_text = font.render("Play as Black", True, WHITE)
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

        # Store rectangles for click detection
        self.white_button_rect = white_button_rect
        self.black_button_rect = black_button_rect
        self.random_button_rect = random_button_rect

    def handle_clicks(self, pos):
        # Handling clicks for AI level dropdown
        if self.ai_level_dropdown_rect.collidepoint(pos):
            self.ai_level_dropdown_selected_index = (self.ai_level_dropdown_selected_index + 1) % len(self.ai_levels)
            return
