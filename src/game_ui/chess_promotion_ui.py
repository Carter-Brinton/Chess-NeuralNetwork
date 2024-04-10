import chess
import pygame
from constants.constants import *


class ChessPromotionUI:
    def __init__(self, chess_ui):
        self.chess_ui = chess_ui

    def draw_promotion_ui(self, pawn_square, player_color):
        self.chess_ui.draw_overlay()
        # Calculate popup position and size
        popup_width = 300
        popup_height = 150
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2

        # Draw the popup background
        pygame.draw.rect(
            self.chess_ui.screen, WHITE, (popup_x, popup_y, popup_width, popup_height)
        )

        # Load images for each promotion option
        promotion_options = ["Queen", "Rook", "Bishop", "Knight"]
        option_buttons = []
        option_height = popup_height // 2  # Example adjustment

        option_width = popup_width // len(promotion_options)
        start_x = (
            popup_x + (popup_width - option_width * len(promotion_options)) // 2
        )  # Calculate starting x position to center options as a group

        for i, option in enumerate(promotion_options):
            option_x = start_x + (i * option_width)
            option_y = (
                popup_y + (popup_height - option_height - 25) // 2
            )  # Adjust to leave space for "Cancel" button

            # Draw option button
            option_rect = pygame.Rect(option_x, option_y, option_width, option_height)
            pygame.draw.rect(self.chess_ui.screen, WHITE, option_rect)
            piece_image = self.chess_ui.my_chess_board.PIECES[
                (("W" if player_color == chess.WHITE else "B") + option)
            ]
            image_x = option_x + (option_width - piece_image.get_width()) // 2
            image_y = option_y + (option_height - piece_image.get_height()) // 2
            self.chess_ui.screen.blit(piece_image, (image_x, image_y))

            option_buttons.append(option_rect)

        self.promotion_option_buttons = option_buttons

        # Drawing the "Cancel" button
        button_width = 100
        button_height = 30
        button_x = (WINDOW_WIDTH - button_width) // 2  # Center horizontally
        button_y = popup_y + popup_height - 40
        cancel_promotion_button_rect = pygame.Rect(
            button_x, button_y, button_width, button_height
        )

        pygame.draw.rect(self.chess_ui.screen, GREY, cancel_promotion_button_rect)
        font = pygame.font.SysFont(None, 24)
        text = font.render("Cancel", True, BLACK)
        text_rect = text.get_rect(
            center=(button_x + button_width // 2, button_y + button_height // 2)
        )
        self.chess_ui.screen.blit(text, text_rect)

        # Store the rectangle for click detection
        self.cancel_promotion_button_rect = cancel_promotion_button_rect

        return option_buttons