import random
import pygame
import chess

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
BOARD_SIZE = 480
SQUARE_SIZE = BOARD_SIZE // 8
OFFSET_X = 100
OFFSET_Y = (WINDOW_HEIGHT - BOARD_SIZE) // 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
BLUE = pygame.Color("blue")
GREEN = pygame.Color("green")
PALEGREEN = pygame.Color("palegreen")
RED = pygame.Color("red")

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Chess Game')

def load_images():
    pieces = ['Pawn', 'Knight', 'Bishop', 'Rook', 'Queen', 'King']
    images = {}
    for piece in pieces:
        for color in ['White', 'Black']:
            key = color[0].upper() + piece
            images[key] = pygame.transform.scale(pygame.image.load(f"src/assets/images/chess_pieces/{color.lower()}-{piece.lower()}.png"), (SQUARE_SIZE, SQUARE_SIZE))
    return images

class ChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.PIECES = load_images()
        self.screen = screen
        self.offset_x, self.offset_y = OFFSET_X, OFFSET_Y
        self.selected_piece = None
        self.legal_moves = list(self.board.legal_moves)
        self.undone_moves = []
        self.scroll_offset = 0
        self.player_color = random.choice([chess.WHITE, chess.BLACK])
        self.show_side_selection = True

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


    def draw_board(self):
        label_font = pygame.font.Font(None, 24)
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
        x, y = pos
        # Adjust column based on player color, to correctly reflect clicks for black players.
        if self.player_color == chess.BLACK:
            col = 7 - (x - self.offset_x) // SQUARE_SIZE
        else:
            col = (x - self.offset_x) // SQUARE_SIZE

        logical_row = 7 - (y - self.offset_y) // SQUARE_SIZE if self.player_color == chess.WHITE else (y - self.offset_y) // SQUARE_SIZE
        square = chess.square(col, logical_row)
        if square in chess.SQUARES:
            return self.select_square(square)
        return False


    def select_square(self, square):
        if square is None:
            return False

        clicked_piece = self.board.piece_at(square)
        if self.selected_piece is not None:
            move = chess.Move(self.selected_piece, square)
            if move in self.legal_moves and (not self.board.is_check() or self.board.is_legal(move)):
                self.board.push(move)
                self.selected_piece = None
                self.legal_moves = list(self.board.legal_moves)
                return True
        elif clicked_piece and clicked_piece.color == self.board.turn:
            self.selected_piece = square
            self.update_legal_moves()
            return True

        self.selected_piece = None
        self.legal_moves = []
        return False

    def update_legal_moves(self):
        if self.board.is_check():
            self.legal_moves = [move for move in self.board.legal_moves if self.board.is_legal(move)]
        else:
            self.legal_moves = [move for move in self.board.legal_moves if move.from_square == self.selected_piece]

    def move_back(self):
        if len(self.board.move_stack) > 0:  # Ensure there are moves to undo
            move = self.board.pop()  # Undo the last move
            self.undone_moves.append(move)  # Store it to allow redo
            self.update_legal_moves()  # Update legal moves list

    def move_forward(self):
        if self.undone_moves:  # Ensure there are moves to redo
            move = self.undone_moves.pop()  # Get the last undone move
            self.board.push(move)  # Redo the move
            self.update_legal_moves()  # Update legal moves list
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.show_side_selection:
                    if self.white_button_rect.collidepoint(event.pos):
                        self.player_color = chess.WHITE
                        self.show_side_selection = False
                    elif self.black_button_rect.collidepoint(event.pos):
                        self.player_color = chess.BLACK
                        self.show_side_selection = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.handle_mouse_click(pos)
                    if self.back_button_rect.collidepoint(event.pos):
                        self.move_back()
                    elif self.forward_button_rect.collidepoint(event.pos):
                        self.move_forward()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.scroll_offset += 20  # Scroll down
                    elif event.key == pygame.K_UP:
                        self.scroll_offset -= 20  # Scroll up

            self.screen.fill(WHITE)
            self.draw_board()
            self.draw_pieces()
            self.draw_ui()
            if self.show_side_selection:
                self.draw_start_game_popup()
            pygame.display.flip()


if __name__ == "__main__":
    game = ChessGame()
    game.run()

pygame.quit()
