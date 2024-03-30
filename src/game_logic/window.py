# window.py
import pygame
import chess
from game_logic.board import ChessBoard  # Update the path as necessary
from constants.constants import *

class ChessWindow:
    def __init__(self, pieces):
        pygame.display.set_caption('Chess')
        self.screen = pygame.display.set_mode((WINDOW_SIZE))

        # Correctly calculate offsets considering the BOARD_PADDING and BOARD_BORDER
        self.vertical_offset = BOARD_PADDING + BOARD_BORDER
        self.horizontal_offset = BOARD_PADDING + BOARD_BORDER

        self.chess_board = ChessBoard(pieces, self.screen, self.horizontal_offset, self.vertical_offset)
        self.clock = pygame.time.Clock() 
        self.moves_log = []  # To keep track of moves

    def draw_interface(self):
        # Starting x-coordinate of the interface is right after the board
        interface_x_start = BOARD_SIZE
        # Draw the interface background
        pygame.draw.rect(self.screen, pygame.Color(INTERFACE_BACKGROUND_COLOR), pygame.Rect(interface_x_start, 0, INTERFACE_WIDTH, WINDOW_SIZE[1]))
        # Add your interface elements here, using interface_x_start as the starting x-coordinate


    def add_move_to_log(self, move):
        # Add moves to the log and handle the display
        pass

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Use the offsets stored in the object
                    adjusted_pos = (pygame.mouse.get_pos()[0] - self.horizontal_offset, pygame.mouse.get_pos()[1] - self.vertical_offset)
                    clicked_square = self.chess_board.square_from_mouse_pos(adjusted_pos)
                    valid_move = self.chess_board.handle_mouse_clicks(clicked_square)
                    if valid_move:
                        self.add_move_to_log(valid_move)

            self.screen.fill(pygame.Color('white'))
            self.chess_board.draw_board()  # Ensure draw_board and draw_pieces do not require offset parameters anymore
            self.chess_board.draw_pieces()
            self.draw_interface()
            pygame.display.flip()
            self.clock.tick(FPS)
