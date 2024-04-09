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
        self.cancel_promotion = False

    def draw_overlay(self):
        overlay_color = (0, 0, 0, 128)
        screen_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        screen_overlay.fill(overlay_color)
        self.screen.blit(screen_overlay, (0, 0))

    def draw_start_game_popup(self):
        self.draw_overlay()

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

    def draw_promotion_ui(self, pawn_square, player_color):
        self.draw_overlay()
        # Calculate popup position and size
        popup_width = 300
        popup_height = 150
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2

        # Draw the popup background
        pygame.draw.rect(self.screen, WHITE, (popup_x, popup_y, popup_width, popup_height))

        # Load images for each promotion option
        promotion_options = ['Queen', 'Rook', 'Bishop', 'Knight']
        option_buttons = []
        option_height = popup_height // 2  # Example adjustment

        option_width = popup_width // len(promotion_options)
        start_x = popup_x + (popup_width - option_width * len(promotion_options)) // 2  # Calculate starting x position to center options as a group

        for i, option in enumerate(promotion_options):
            option_x = start_x + (i * option_width)
            option_y = popup_y + (popup_height - option_height - 25) // 2  # Adjust to leave space for "Cancel" button

            # Draw option button
            option_rect = pygame.Rect(option_x, option_y, option_width, option_height)
            pygame.draw.rect(self.screen, WHITE, option_rect)
            piece_image = self.my_chess_board.PIECES[(('W' if player_color == chess.WHITE else 'B') + option)]
            image_x = option_x + (option_width - piece_image.get_width()) // 2
            image_y = option_y + (option_height - piece_image.get_height()) // 2
            self.screen.blit(piece_image, (image_x, image_y))

            option_buttons.append(option_rect)

        self.promotion_option_buttons = option_buttons

        # Drawing the "Cancel" button
        button_width = 100
        button_height = 30
        button_x = (WINDOW_WIDTH - button_width) // 2  # Center horizontally
        button_y = popup_y + popup_height - 40
        cancel_promotion_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        pygame.draw.rect(self.screen, GREY, cancel_promotion_button_rect)
        font = pygame.font.SysFont(None, 24)
        text = font.render('Cancel', True, BLACK)
        text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        self.screen.blit(text, text_rect)

        # Store the rectangle for click detection
        self.cancel_promotion_button_rect = cancel_promotion_button_rect

        return option_buttons

    def draw_forward_and_back_ui(self, ui_x_start, ui_y_start):
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

    def draw_restart_game_button(self, ui_x_start, ui_y_start, ui_height):
        button_width = 110
        button_height = 30

        # Create restart button
        self.restart_button_rect = pygame.Rect(ui_x_start, ui_y_start + ui_height + 10, button_width, button_height)
        pygame.draw.rect(self.screen, pygame.Color("darkgrey"), self.restart_button_rect)
        font = pygame.font.Font(None, 22)
        text = font.render('Restart Game', True, BLACK)
        text_rect = text.get_rect(center=self.restart_button_rect.center)
        self.screen.blit(text, text_rect)

        # Create quit button
        self.quit_button_rect = pygame.Rect(ui_x_start + (button_width + 5),  ui_y_start + ui_height + 10, button_width, button_height)
        pygame.draw.rect(self.screen, pygame.Color("darkgrey"), self.quit_button_rect)
        text = font.render('Quit Game', True, BLACK)
        text_rect = text.get_rect(center=self.quit_button_rect.center)
        self.screen.blit(text, text_rect)

    def draw_move_tracking_ui(self):
        ui_background_color = pygame.Color("lightblue")
        ui_x_start = OFFSET_X + BOARD_SIZE + 15
        ui_y_start = 58
        ui_width = 225
        ui_height = 184

        # Draw UI background with adjusted dimensions
        pygame.draw.rect(self.screen, ui_background_color, (ui_x_start, ui_y_start, ui_width, ui_height))

        self.draw_forward_and_back_ui(ui_x_start, ui_y_start)
        self.draw_restart_game_button(ui_x_start, ui_y_start, ui_height)

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