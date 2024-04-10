import chess
import pygame
from constants.constants import *

class ChessMiscUI:
    def __init__(self, chess_ui):
        self.chess_ui = chess_ui

    def draw_overlay(self):
        overlay_color = (0, 0, 0, 128)
        screen_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        screen_overlay.fill(overlay_color)
        self.chess_ui.screen.blit(screen_overlay, (0, 0))

    def draw_gradient_left_to_right(self, rect, start_color, end_color):
        colour_rect = pygame.Surface((2, 2))
        pygame.draw.line(colour_rect, start_color, (0, 0), (0, 1))
        pygame.draw.line(colour_rect, end_color, (1, 0), (1, 1))
        colour_rect = pygame.transform.smoothscale(
            colour_rect, (rect.width, rect.height)
        )
        self.chess_ui.screen.blit(colour_rect, rect)

    def draw_gradient_text(self, text, font, rect, start_color, end_color):
        text_surf = font.render(text, True, start_color)  # Render text to get size
        x, y, width, height = rect
        text_width, text_height = text_surf.get_size()
        x_start = x + (width - text_width) // 2  # Center text in rect
        y_start = y + (height - text_height) // 2

        for i, letter in enumerate(text):
            # Calculate color for each letter
            color_fraction = i / len(text)
            color = [
                (end_color[j] - start_color[j]) * color_fraction + start_color[j]
                for j in range(3)
            ]
            letter_surf = font.render(letter, True, color)

            # Blit each letter individually
            self.chess_ui.screen.blit(letter_surf, (x_start, y_start))
            x_start += letter_surf.get_width()  # Move to the right for the next letter
