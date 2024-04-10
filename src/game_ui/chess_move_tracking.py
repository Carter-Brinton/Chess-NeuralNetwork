# chess_ui.py
import chess
import pygame
from constants.constants import *


class ChessMoveTrackingUI:
    def __init__(self, chess_ui):
        self.chess_ui = chess_ui

    def draw_forward_and_back_ui(self, ui_x_start, ui_y_start):
        back_button_color = pygame.Color("grey")
        forward_button_color = pygame.Color("grey")
        self.back_button_rect = pygame.Rect(ui_x_start + 25, ui_y_start - 40, 80, 30)
        self.forward_button_rect = pygame.Rect(
            ui_x_start + 120, ui_y_start - 40, 80, 30
        )

        pygame.draw.rect(self.chess_ui.screen, back_button_color, self.back_button_rect)
        pygame.draw.rect(self.chess_ui.screen, forward_button_color, self.forward_button_rect)

        # Adding text to the buttons
        button_font = pygame.font.Font(None, 21)
        back_text = button_font.render("Back", True, BLACK)
        forward_text = button_font.render("Forward", True, BLACK)
        self.chess_ui.screen.blit(
            back_text, (self.back_button_rect.x + 22, self.back_button_rect.y + 8)
        )
        self.chess_ui.screen.blit(
            forward_text,
            (self.forward_button_rect.x + 12, self.forward_button_rect.y + 8),
        )

    def draw_move_tracking_ui(self):
        ui_background_color = pygame.Color("lightblue")
        ui_x_start = OFFSET_X + BOARD_SIZE + 15
        ui_y_start = 58
        ui_width = 225
        ui_height = 184

        # Draw UI background with adjusted dimensions
        pygame.draw.rect(
            self.chess_ui.screen,
            ui_background_color,
            (ui_x_start, ui_y_start, ui_width, ui_height),
        )

        self.draw_forward_and_back_ui(ui_x_start, ui_y_start)
        self.chess_ui.draw_restart_game_button(ui_x_start, ui_y_start, ui_height)

        # Set up the table headers
        font = pygame.font.Font(None, 25)
        headers = ["Turn", "White", "Black"]
        header_x_start = ui_x_start + 10
        header_y_start = ui_y_start + 10

        # Draw headers outside the clipping area to keep them static
        for i, header in enumerate(headers):
            text_surface = font.render(header, True, BLACK)
            self.chess_ui.screen.blit(
                text_surface, (header_x_start + i * 75, header_y_start)
            )  # Adjust column spacing here

        # Define a clipping area for the moves list
        clip_rect = pygame.Rect(
            ui_x_start, header_y_start + 30, ui_width, ui_height - 40
        )
        self.chess_ui.screen.set_clip(clip_rect)  # Set the clipping area

        move_step = 20
        move_log_y_start = (
            header_y_start + 30
        )  # Start displaying moves a bit below the headers
        turn_count = len(self.chess_ui.board.move_stack) // 2 + 1
        for i in range(turn_count):
            turn_number = str(i + 1)
            white_move = (
                str(self.chess_ui.board.move_stack[i * 2])
                if i * 2 < len(self.chess_ui.board.move_stack)
                else ""
            )
            black_move = (
                str(self.chess_ui.board.move_stack[i * 2 + 1])
                if i * 2 + 1 < len(self.chess_ui.board.move_stack)
                else ""
            )

            turn_surface = font.render(turn_number, True, BLACK)
            white_move_surface = font.render(white_move, True, BLACK)
            black_move_surface = font.render(black_move, True, BLACK)

            y_position = move_log_y_start + i * move_step - self.chess_ui.scroll_offset
            self.chess_ui.screen.blit(turn_surface, (header_x_start + 10, y_position))
            self.chess_ui.screen.blit(white_move_surface, (header_x_start + 76, y_position))
            self.chess_ui.screen.blit(black_move_surface, (header_x_start + 152, y_position))

        # Remove clipping to draw the rest of the UI normally
        self.chess_ui.screen.set_clip(None)

        # Adjust scroll offset for next frame
        max_scroll = max(0, turn_count * move_step - (ui_height - header_y_start - 20))
        self.chess_ui.scroll_offset = max(0, min(self.chess_ui.scroll_offset, max_scroll))
