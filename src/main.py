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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.show_start_game_popup:
                        # Handle start game popup interactions
                        if self.my_chess_ui.white_button_rect.collidepoint(event.pos):
                            self.player_color = chess.WHITE
                            self.show_start_game_popup = False
                            self.my_chess_board.update_player_color(chess.WHITE)
                        elif self.my_chess_ui.black_button_rect.collidepoint(event.pos):
                            self.player_color = chess.BLACK
                            self.show_start_game_popup = False
                            self.my_chess_board.update_player_color(chess.BLACK)
                    elif self.my_chess_board.awaiting_promotion:
                        # Handle promotion piece selection
                        for option_rect, promotion_piece in zip(self.my_chess_ui.promotion_option_buttons, [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]):
                            if option_rect.collidepoint(event.pos):
                                move = chess.Move(self.my_chess_board.selected_piece, self.my_chess_board.square_to_promote, promotion=promotion_piece)
                                if move in self.my_chess_board.legal_moves:
                                    self.board.push(move)
                                    self.my_chess_board.awaiting_promotion = False
                                    self.my_chess_board.selected_piece = None
                                    self.my_chess_board.legal_moves = list(self.board.legal_moves)
                                    self.my_chess_board.awaiting_promotion = False
                                    break
                    else:
                        # Handle regular game interactions
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

            # Redraw the game state
            self.screen.fill(WHITE)
            self.my_chess_board.draw_board()
            self.my_chess_board.draw_pieces()
            self.my_chess_ui.draw_move_tracking_ui()

            if self.my_chess_board.awaiting_promotion:
                self.my_chess_ui.draw_promotion_ui(None, self.board.piece_at(self.my_chess_board.selected_piece).color)

            if self.show_start_game_popup:
                self.my_chess_ui.draw_start_game_popup()

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Chess Game')
    game = ChessGame(screen)
    game.run()