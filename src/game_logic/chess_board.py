# chess_board.py
import chess
from constants.constants import *
import time

class ChessBoard:
    def __init__(self, screen, PIECES, player_color, offset_x, offset_y, board):
        self.screen = screen
        self.PIECES = PIECES
        self.player_color = player_color
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.board = board
        self.legal_moves = list(self.board.legal_moves)
        self.selected_piece = None
        self.undone_moves = []
        self.awaiting_promotion = False
        self.square_to_promote = None
        self.playing_against_ai = False
        self.ai_color = None
        self.is_ai_turn = False
        self.draw_ai_moves = False

    def update_player_color(self, player_color):
        self.player_color = player_color
        if(self.playing_against_ai):
            self.ai_color = chess.WHITE if self.player_color == chess.BLACK else chess.BLACK
            if(self.ai_color == chess.WHITE):
                self.is_ai_turn = True

    def reset(self):
        self.legal_moves = list(self.board.legal_moves)
        self.selected_piece = None
        self.undone_moves = []
        self.awaiting_promotion = False
        self.square_to_promote = None
            
    def make_ai_vs_ai_move(self, move_uci):
        move = chess.Move.from_uci(move_uci)
        if move in self.board.legal_moves:
            self.board.push(move)
        else:
            # print("AI attempted an illegal move:", move_uci)
            pass
        self.draw_ai_moves = True
        # time.sleep(.1)

    def make_ai_vs_player_move(self, move_uci):
        move = chess.Move.from_uci(move_uci)
        if move in self.board.legal_moves:
            self.board.push(move)
        else:
            # print("AI attempted an illegal move:", move_uci)
            pass
        self.is_ai_turn = False
        self.draw_ai_moves = True
        time.sleep(.1)

    def draw_board(self):
        label_font = pygame.font.Font(None, 24)
        move_text_font = pygame.font.Font(None, 30) 
        player_color = 'WHITE' if self.board.turn == chess.WHITE else 'BLACK'
        move_text = f"Player '{player_color}' to Move"
        move_text_surface = move_text_font.render(move_text, True, BLACK)

        # Calculate the position to center the text above the board
        text_x = self.offset_x + (BOARD_SIZE - move_text_surface.get_width()) // 2
        text_y = self.offset_y - move_text_surface.get_height() - 20  # 20 pixels above the board
        self.screen.blit(move_text_surface, (text_x, text_y))

        border_thickness = 2
        pygame.draw.rect(self.screen, BLACK, (self.offset_x - border_thickness,
                                              self.offset_y - border_thickness,
                                              BOARD_SIZE + border_thickness * 2,
                                              BOARD_SIZE + border_thickness * 2),
                         border_thickness)

        colors = [WHITE, GREY]
        for r in range(8):
            for c in range(8):
                color = colors[((r + c) % 2)]
                pygame.draw.rect(self.screen, color, (c * SQUARE_SIZE + self.offset_x, r * SQUARE_SIZE + self.offset_y, SQUARE_SIZE, SQUARE_SIZE))

        for i in range(8):
            rank_label = str(8 - i) if self.player_color == chess.WHITE else str(i + 1)
            file_label = chr(ord('a') + i) if self.player_color == chess.WHITE else chr(ord('h') - i)

            # Draw rank labels (1-8)
            rank_label_surface = label_font.render(rank_label, True, BLACK)
            self.screen.blit(rank_label_surface, (self.offset_x - 20, i * SQUARE_SIZE + self.offset_y + SQUARE_SIZE // 2 - rank_label_surface.get_height() // 2))

            # Draw file labels (a-h)
            file_label_surface = label_font.render(file_label, True, BLACK)
            self.screen.blit(file_label_surface, (i * SQUARE_SIZE + self.offset_x + SQUARE_SIZE // 2 - file_label_surface.get_width() // 2, self.offset_y + BOARD_SIZE + 5))

    def draw_pieces(self):
        # Adjusted to ensure pieces are drawn correctly based on player's perspective.
        for r in range(8):
            for c in range(8):
                square = chess.square(c, r if self.player_color == chess.BLACK else 7-r)
                piece = self.board.piece_at(square)
                if piece:
                    color = 'White' if piece.color else 'Black'
                    piece_name = {chess.PAWN: 'Pawn', chess.KNIGHT: 'Knight', chess.BISHOP: 'Bishop', chess.ROOK: 'Rook', chess.QUEEN: 'Queen', chess.KING: 'King'}[piece.piece_type]
                    piece_key = color[0].upper() + piece_name
                    self.screen.blit(self.PIECES[piece_key], ((c if self.player_color == chess.WHITE else 7-c) * SQUARE_SIZE + self.offset_x, r * SQUARE_SIZE + self.offset_y))

        self.highlight_moves()

    def highlight_moves(self):
        if self.selected_piece is not None:
            self.draw_selected_piece()
            self.draw_legal_moves()
            self.draw_capture_highlights()
        self.check_indication()
        self.castling_highlights()

    def draw_selected_piece(self):
        selected_col, selected_row = self.selected_piece % 8, self.selected_piece // 8
        if self.player_color == chess.BLACK:
            visual_col, visual_row = 7 - selected_col, selected_row
        else:
            visual_col, visual_row = selected_col, 7 - selected_row

        pygame.draw.rect(self.screen, BLUE, (visual_col * SQUARE_SIZE + self.offset_x, visual_row * SQUARE_SIZE + self.offset_y, SQUARE_SIZE, SQUARE_SIZE), 3)

    def draw_legal_moves(self):
        for move in self.legal_moves:
            if move.from_square == self.selected_piece:
                to_col = move.to_square % 8
                to_row = move.to_square // 8
                # Adjust both row and column based on player color (Same logic for drawing methods below)
                if self.player_color == chess.BLACK:
                    draw_to_col = 7 - to_col  # Invert column for black
                    draw_to_row = to_row      # Row is already correctly adjusted for both perspectives
                else:
                    draw_to_col = to_col      # No column adjustment needed for white
                    draw_to_row = 7 - to_row  # Invert row for white

                center_x = draw_to_col * SQUARE_SIZE + SQUARE_SIZE // 2 + self.offset_x
                center_y = draw_to_row * SQUARE_SIZE + SQUARE_SIZE // 2 + self.offset_y
                pygame.draw.circle(self.screen, PALEGREEN, (center_x, center_y), SQUARE_SIZE // 10)

    def draw_capture_highlights(self):
        for move in self.legal_moves:
            if self.board.is_capture(move):
                target_square = move.to_square
                target_col = target_square % 8
                target_row = target_square // 8
                if self.player_color == chess.BLACK:
                    draw_target_col = 7 - target_col
                    draw_target_row = target_row
                else:
                    draw_target_col = target_col
                    draw_target_row = 7 - target_row

                pygame.draw.rect(self.screen, RED, (draw_target_col * SQUARE_SIZE + self.offset_x, draw_target_row * SQUARE_SIZE + self.offset_y, SQUARE_SIZE, SQUARE_SIZE), 3)

    def check_indication(self):
        king_square = self.board.king(self.board.turn)
        if king_square is not None and self.board.is_check():
            king_col, king_row = king_square % 8, king_square // 8
            if self.player_color == chess.BLACK:
                draw_king_col = 7 - king_col
                draw_king_row = king_row
            else:
                draw_king_col = king_col
                draw_king_row = 7 - king_row

            pygame.draw.rect(self.screen, RED, (draw_king_col * SQUARE_SIZE + self.offset_x, draw_king_row * SQUARE_SIZE + self.offset_y, SQUARE_SIZE, SQUARE_SIZE), 3)

    def castling_highlights(self):
        if self.selected_piece is not None and self.board.piece_at(self.selected_piece) and self.board.piece_at(self.selected_piece).piece_type == chess.KING:
            for move in self.legal_moves:
                if self.board.is_castling(move):
                    rook_pos = move.to_square
                    is_queenside = rook_pos < self.selected_piece
                    castling_col = 2 if is_queenside else 6
                    castling_row = 0 if self.board.turn == chess.WHITE else 7
                    if self.player_color == chess.BLACK:
                        draw_castling_col = 7 - castling_col
                        draw_castling_row = castling_row
                    else:
                        draw_castling_col = castling_col
                        draw_castling_row = 7 - castling_row

                    pygame.draw.rect(self.screen, GREEN, (draw_castling_col * SQUARE_SIZE + self.offset_x, draw_castling_row * SQUARE_SIZE + self.offset_y, SQUARE_SIZE, SQUARE_SIZE), 3)
        
    def handle_mouse_click(self, pos):
        if self.is_ai_turn:
            return False
    
        x, y = pos
        # Adjust column based on player color, to correctly reflect clicks for black players.
        if self.player_color == chess.BLACK:
            col = 7 - (x - self.offset_x) // SQUARE_SIZE
        else:
            col = (x - self.offset_x) // SQUARE_SIZE

        logical_row = 7 - (y - self.offset_y) // SQUARE_SIZE if self.player_color == chess.WHITE else (y - self.offset_y) // SQUARE_SIZE
        square = chess.square(col, logical_row)
        if square in chess.SQUARES:
            successful_move = self.select_square_to_move_to(square)
            if successful_move:
                if(self.playing_against_ai):
                    self.is_ai_turn = True
                self.undone_moves.clear()
            return successful_move
        return False

    def select_square_to_move_to(self, square):
        if square is None:
            return False

        clicked_piece = self.board.piece_at(square)
        if self.selected_piece is not None and self.selected_piece != square:
            move = chess.Move(self.selected_piece, square)
            # Check if the move is a promotion
            if self.board.piece_at(self.selected_piece).piece_type == chess.PAWN:
                promotion_rank = 7 if self.board.piece_at(self.selected_piece).color == chess.WHITE else 0
                if chess.square_rank(square) == promotion_rank:
                    self.awaiting_promotion = True
                    self.square_to_promote = square
                    return False  # Awaiting promotion selection

            if move in self.legal_moves and (not self.board.is_check() or self.board.is_legal(move)):
                self.board.push(move)
                self.selected_piece = None
                self.legal_moves = list(self.board.legal_moves)
                self.awaiting_promotion = False
                return True
            elif clicked_piece and clicked_piece.color == self.board.turn:
                self.selected_piece = square
                self.update_legal_moves()
                return False  # Return False to indicate no move was made, but selection has changed
        elif clicked_piece and clicked_piece.color == self.board.turn:
            self.selected_piece = square
            self.update_legal_moves()
            return False 

        self.selected_piece = None
        self.legal_moves = []
        self.awaiting_promotion = False
        return False

    def update_legal_moves(self):
        if self.board.is_check():
            self.legal_moves = [move for move in self.board.legal_moves if self.board.is_legal(move)]
        else:
            self.legal_moves = [move for move in self.board.legal_moves if move.from_square == self.selected_piece]

    def move_back(self):
        if len(self.board.move_stack) > 0:
            move = self.board.pop()
            self.undone_moves.append(move)
            self.update_legal_moves()

    def move_forward(self):
        if self.undone_moves:
            move = self.undone_moves.pop()
            self.board.push(move)
            self.update_legal_moves()
