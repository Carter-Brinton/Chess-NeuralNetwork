import chess
import pygame
from constants.constants import *


class ChessPlayAIUI:
    def __init__(self, chess_ui):
        self.chess_ui = chess_ui
        self.ai_levels = ["1 (Easy)", "2 (Less Easy)", "3 (Medium)", "4 (Less Hard)", "5 (Hard)"]
        self.current_level_index = 0  # Start with the first level, "Easy"

    def draw_ai_level_selector(self):
        # Popup dimensions and position
        popup_x = (WINDOW_WIDTH - 300) // 2
        # Position the AI level selector above the starting color buttons
        popup_y = (WINDOW_HEIGHT - 290) // 2 - 60  
        
        # Define the AI level button rectangle
        ai_level_button_rect = pygame.Rect(popup_x + 50, popup_y, 200, 50)
        
        # Draw the button background
        pygame.draw.rect(self.chess_ui.screen, PALEBLUE, ai_level_button_rect)
        # Optionally draw a border for the button
        pygame.draw.rect(self.chess_ui.screen, BLACK, ai_level_button_rect, 2)
        
        # Define font and render the current AI level text
        font = pygame.font.Font(None, 30)
        current_level_text = self.ai_levels[self.current_level_index]
        level_text_surface = font.render(current_level_text, True, BLACK)
        
        # Calculate text position for center alignment within the button
        text_x = ai_level_button_rect.x + (ai_level_button_rect.width - level_text_surface.get_width()) // 2
        text_y = ai_level_button_rect.y + (ai_level_button_rect.height - level_text_surface.get_height()) // 2
        
        # Blit the text surface onto the screen
        self.chess_ui.screen.blit(level_text_surface, (text_x, text_y))
        
        # Store the rectangle for click detection
        self.ai_level_button_rect = ai_level_button_rect

    def handle_ai_level_click(self, pos):
        # Check if the AI level button was clicked
        if self.ai_level_button_rect.collidepoint(pos):
            # Cycle through the AI levels
            self.current_level_index = (self.current_level_index + 1) % len(self.ai_levels)
            # Redraw the UI to reflect the updated level
            self.draw_select_starting_color_ui()
            self.draw_ai_level_selector()
        
    def draw_select_starting_color_ui(self):
        self.chess_ui.draw_overlay()
        self.draw_ai_level_selector()

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