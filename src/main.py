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
            self.board = chess.Board()
            self.screen = screen
            self.PIECES = load_images()
            self.offset_x, self.offset_y = OFFSET_X, OFFSET_Y
            self.show_start_game_popup = True
            self.player_color = random.choice([chess.WHITE, chess.BLACK])
            self.my_chess_board = ChessBoard(self.screen, self.PIECES, self.player_color, self.offset_x, self.offset_y, self.board)
            self.my_chess_ui = ChessUI(self.screen, self.my_chess_board, self.board)
            
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.show_start_game_popup:
                    if self.my_chess_ui.white_button_rect.collidepoint(event.pos):
                        self.player_color = chess.WHITE
                        self.show_start_game_popup = False
                        self.my_chess_board.update_player_color(chess.WHITE)
                    elif self.my_chess_ui.black_button_rect.collidepoint(event.pos):
                        self.player_color = chess.BLACK
                        self.show_start_game_popup = False
                        self.my_chess_board.update_player_color(chess.BLACK) 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.my_chess_board.handle_mouse_click(pos)
                    if self.my_chess_ui.back_button_rect.collidepoint(event.pos):
                        self.my_chess_board.move_back()
                    elif self.my_chess_ui.forward_button_rect.collidepoint(event.pos):
                        self.my_chess_board.move_forward()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.my_chess_ui.scroll_offset += 20  # Scroll down
                    elif event.key == pygame.K_UP:
                        self.my_chess_ui.scroll_offset -= 20  # Scroll up

            self.screen.fill(WHITE)
            self.my_chess_board.draw_board()  # Call draw_board on the ChessBoard instance
            self.my_chess_board.draw_pieces()  # Similarly, ensure draw_pieces is called on the ChessBoard instance
            self.my_chess_ui.draw_ui()  # Assuming draw_ui is a method of the ChessUI class
            if self.show_start_game_popup:
                self.my_chess_ui.draw_start_game_popup()  # Assuming this is intended to be part of the UI

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Chess Game')
    game = ChessGame(screen)
    game.run()