import pygame
import sys
import os
from game_logic.board import Board  # Ensure your import matches the actual file structure
from constants.constants import *

pygame.init()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, BOARD_HEIGHT))
    game_board = Board()

    selected_piece = None
    selected_pos = None
    valid_moves = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if game_board.handle_mouse_click(mouse_x, mouse_y):  # This method now manages clicks
                    selected_piece, selected_pos, valid_moves = game_board.get_selected_state()

        game_board.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
