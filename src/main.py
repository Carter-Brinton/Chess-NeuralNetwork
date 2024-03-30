# main.py
from constants.constants import *
from game_logic.chess_board import ChessBoard
from game_logic.chess_ui import ChessUI
from utils.load_images import load_images
import chess
import random


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Chess Game')


class ChessGame:
    def __init__(self, screen):
        self.screen = screen
        self.PIECES = load_images()
        self.board = ChessBoard(self.screen, self.PIECES) 
        self.ui = ChessUI(self.screen, self.board)
        self.offset_x, self.offset_y = OFFSET_X, OFFSET_Y
        self.selected_piece = None
        self.legal_moves = list(self.board.legal_moves)
        self.player_color = chess.WHITE 
        self.undone_moves = []
        self.scroll_offset = 0
        self.player_color = random.choice([chess.WHITE, chess.BLACK])
        self.show_side_selection = True

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.show_side_selection:
                    if self.ui.white_button_rect.collidepoint(event.pos):
                        self.player_color = chess.WHITE
                        self.show_side_selection = False
                    elif self.ui.black_button_rect.collidepoint(event.pos):
                        self.player_color = chess.BLACK
                        self.show_side_selection = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.board.handle_mouse_click(pos)
                    if self.ui.back_button_rect.collidepoint(event.pos):
                        self.board.move_back()
                    elif self.ui.forward_button_rect.collidepoint(event.pos):
                        self.board.move_forward()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.scroll_offset += 20  # Scroll down
                    elif event.key == pygame.K_UP:
                        self.scroll_offset -= 20  # Scroll up

            self.screen.fill(WHITE)
            self.board.draw_board()  # Call draw_board on the ChessBoard instance
            self.board.draw_pieces()  # Similarly, ensure draw_pieces is called on the ChessBoard instance
            self.ui.draw_ui()  # Assuming draw_ui is a method of the ChessUI class
            if self.show_side_selection:
                self.ui.draw_start_game_popup()  # Assuming this is intended to be part of the UI

            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Chess Game')
    game = ChessGame(screen)
    game.run()