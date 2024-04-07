# chess_ui.py
import chess
import pygame
from constants.constants import *

class ChessUI:
    def __init__(self, screen, my_chess_board, board):
        self.screen = screen
        self.my_chess_board = my_chess_board
        self.board = board
        self.scroll_offset = 0  

    def draw_start_game_popup(self):
        overlay_color = (0, 0, 0, 128)
        screen_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        screen_overlay.fill(overlay_color)
        self.screen.blit(screen_overlay, (0, 0))

        # Popup dimensions and position
        popup_width = 300
        popup_height = 200
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2
        
        # Popup background
        pygame.draw.rect(self.screen, GREY, (popup_x, popup_y, popup_width, popup_height))
        
        # Draw buttons or text options for selecting sides
        font = pygame.font.Font(None, 36)
        white_button_rect = pygame.Rect(popup_x + 50, popup_y + 50, 200, 50)
        black_button_rect = pygame.Rect(popup_x + 50, popup_y + 120, 200, 50)
        
        pygame.draw.rect(self.screen, WHITE, white_button_rect)
        pygame.draw.rect(self.screen, BLACK, black_button_rect)
        
        white_text = font.render('Play as White', True, BLACK)
        black_text = font.render('Play as Black', True, WHITE)
        self.screen.blit(white_text, (white_button_rect.x + 20, white_button_rect.y + 10))
        self.screen.blit(black_text, (black_button_rect.x + 20, black_button_rect.y + 10))
        
        # Store rectangles for click detection
        self.white_button_rect = white_button_rect
        self.black_button_rect = black_button_rect

    def draw_ui_buttons(self, ui_x_start, ui_y_start):
        back_button_color = pygame.Color("grey")
        forward_button_color = pygame.Color("grey")
        self.back_button_rect = pygame.Rect(ui_x_start + 25, ui_y_start - 40, 80, 30)
        self.forward_button_rect = pygame.Rect(ui_x_start + 120, ui_y_start - 40, 80, 30)

        pygame.draw.rect(self.screen, back_button_color, self.back_button_rect)
        pygame.draw.rect(self.screen, forward_button_color, self.forward_button_rect)

        # Adding text to the buttons
        button_font = pygame.font.Font(None, 21)
        back_text = button_font.render('Back', True, BLACK)
        forward_text = button_font.render('Forward', True, BLACK)
        self.screen.blit(back_text, (self.back_button_rect.x + 22, self.back_button_rect.y + 8))
        self.screen.blit(forward_text, (self.forward_button_rect.x + 12, self.forward_button_rect.y + 8))


    def draw_ui(self):
        ui_background_color = pygame.Color("lightblue")
        ui_x_start = OFFSET_X + BOARD_SIZE + 15
        ui_y_start = 58
        ui_width = 225
        ui_height = 184

        # Draw UI background with adjusted dimensions
        pygame.draw.rect(self.screen, ui_background_color, (ui_x_start, ui_y_start, ui_width, ui_height))

        self.draw_ui_buttons(ui_x_start, ui_y_start)

        # Set up the table headers
        font = pygame.font.Font(None, 25)
        headers = ["Turn", "White", "Black"]
        header_x_start = ui_x_start + 10
        header_y_start = ui_y_start + 10 

        # Draw headers outside the clipping area to keep them static
        for i, header in enumerate(headers):
            text_surface = font.render(header, True, BLACK)
            self.screen.blit(text_surface, (header_x_start + i * 75, header_y_start))  # Adjust column spacing here

        # Define a clipping area for the moves list
        clip_rect = pygame.Rect(ui_x_start, header_y_start + 30, ui_width, ui_height - 40)
        self.screen.set_clip(clip_rect)  # Set the clipping area

        move_step = 20
        move_log_y_start = header_y_start + 30  # Start displaying moves a bit below the headers
        turn_count = len(self.board.move_stack) // 2 + 1 
        for i in range(turn_count):
            turn_number = str(i + 1)
            white_move = str(self.board.move_stack[i * 2]) if i * 2 < len(self.board.move_stack) else ""
            black_move = str(self.board.move_stack[i * 2 + 1]) if i * 2 + 1 < len(self.board.move_stack) else ""

            turn_surface = font.render(turn_number, True, BLACK)
            white_move_surface = font.render(white_move, True, BLACK)
            black_move_surface = font.render(black_move, True, BLACK)

            y_position = move_log_y_start + i * move_step - self.scroll_offset
            self.screen.blit(turn_surface, (header_x_start + 10, y_position))
            self.screen.blit(white_move_surface, (header_x_start + 76, y_position))
            self.screen.blit(black_move_surface, (header_x_start + 152, y_position))

        # Remove clipping to draw the rest of the UI normally
        self.screen.set_clip(None)

        # Adjust scroll offset for next frame
        max_scroll = max(0, turn_count * move_step - (ui_height - header_y_start - 20))
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))