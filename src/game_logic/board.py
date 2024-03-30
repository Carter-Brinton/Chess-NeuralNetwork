import pygame
import os
from game_logic.pieces import Rook, Bishop, Knight, Queen, King, Pawn
from constants.constants import *

class Board:
    def __init__(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_turn = 'white'
        self.images = self.load_images()  # Make sure to call this as an instance method
        self.initialize_board()
        self.selected_piece = None
        self.selected_pos = None
        self.valid_moves = []

    def load_images(self):
        images = {}
        pieces = ['rook', 'bishop', 'knight', 'queen', 'king', 'pawn']
        colors = ['white', 'black']
        for color in colors:
            for piece in pieces:
                filename = f"{color}-{piece}.png"
                path = os.path.join("src", "assets", "images", "chess_pieces", filename)
                try:
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
                    images[f"{color}-{piece}"] = image
                except pygame.error as e:
                    print(f"Error loading image: {path}", e)
        return images

    def initialize_board(self):
        for i, piece_class in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
            self.board[0][i] = piece_class('black', self.images[f"black-{piece_class.__name__.lower()}"])
            self.board[7][i] = piece_class('white', self.images[f"white-{piece_class.__name__.lower()}"])

        # Pawns
        for i in range(BOARD_SIZE):
            self.board[1][i] = Pawn('black', self.images["black-pawn"])
            self.board[6][i] = Pawn('white', self.images["white-pawn"])

    def handle_mouse_click(self, x, y):
        # Adjust mouse coordinates to account for the margins and borders
        adjusted_x = x - BOARD_MARGIN - BOARD_BORDER_SIZE
        adjusted_y = y - BOARD_MARGIN - BOARD_BORDER_SIZE

        # Ensure the click is within the bounds of the board
        if adjusted_x < 0 or adjusted_y < 0 or adjusted_x >= BOARD_WIDTH or adjusted_y >= BOARD_HEIGHT:
            self.selected_piece = None
            self.selected_pos = None
            self.valid_moves = []
            return False

        # Convert adjusted mouse coordinates to board grid positions
        grid_x, grid_y = adjusted_x // SQUARE_SIZE, adjusted_y // SQUARE_SIZE
        
        # If a piece is already selected and the click is within the valid moves
        if self.selected_piece and (grid_x, grid_y) in self.valid_moves:
            if isinstance(self.selected_piece, King) and abs(self.selected_pos[0] - grid_x) == 2:
                # Castling move detected, handle rook movement
                self.perform_castling(grid_x, grid_y)
            else:
                # Regular move
                self.move_piece(grid_x, grid_y)
            self.switch_turn()  # Switch turns after a successful move
            self.deselect_piece()
            return True
        elif self.board[grid_y][grid_x] and self.board[grid_y][grid_x].color == self.current_turn:
            # Select a different piece if it's a valid choice
            self.selected_piece = self.board[grid_y][grid_x]
            self.selected_pos = (grid_x, grid_y)
            self.valid_moves = self.selected_piece.get_moves(grid_x, grid_y, self.board)
            return True
        else:
            # Deselect if clicked on an empty square or an invalid move
            return self.select_piece(grid_x, grid_y)

    def move_piece(self, grid_x, grid_y):
        # Move the selected piece to the new position
        self.board[self.selected_pos[1]][self.selected_pos[0]] = None
        self.board[grid_y][grid_x] = self.selected_piece
        self.selected_piece.has_moved = True  # Update has_moved for the piece

    def perform_castling(self, grid_x, grid_y):
        # Calculate the rook's initial and final positions based on the king's move
        rook_x_initial = 0 if grid_x == 2 else 7
        rook_x_final = 3 if grid_x == 2 else 5
        rook = self.board[grid_y][rook_x_initial]
        # Move the rook
        self.board[grid_y][rook_x_initial] = None
        self.board[grid_y][rook_x_final] = rook
        rook.has_moved = True
        # Move the king
        self.move_piece(grid_x, grid_y)

    def deselect_piece(self):
        self.selected_piece = None
        self.selected_pos = None
        self.valid_moves = []

    def select_piece(self, grid_x, grid_y):
        if self.board[grid_y][grid_x] and self.board[grid_y][grid_x].color == self.current_turn:
            self.selected_piece = self.board[grid_y][grid_x]
            self.selected_pos = (grid_x, grid_y)
            self.valid_moves = self.selected_piece.get_moves(grid_x, grid_y, self.board)
            return True
        return False


    def get_selected_state(self):
        return self.selected_piece, self.selected_pos, self.valid_moves

    def reset_game(self):
        self.initialize_board()
        self.current_turn = 'white'

    def draw(self, screen):
        # Fill the background
        screen.fill(WHITE)
        
        # Adjust the starting point and dimensions for the margin
        board_start_x = BOARD_MARGIN + BOARD_BORDER_SIZE
        board_start_y = BOARD_MARGIN + BOARD_BORDER_SIZE
        board_width_with_margin = BOARD_WIDTH + 2 * BOARD_BORDER_SIZE
        board_height_with_margin = BOARD_HEIGHT + 2 * BOARD_BORDER_SIZE
        
        # Draw the board border with margin accounted for
        pygame.draw.rect(screen, BLACK, (BOARD_MARGIN, BOARD_MARGIN, board_width_with_margin, board_height_with_margin))

        # Draw the chess squares
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                color = WHITE if (x + y) % 2 == 0 else GREY
                pygame.draw.rect(screen, color, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if piece:
                    screen.blit(self.images[f"{piece.color}-{piece.type}"], (x * SQUARE_SIZE, y * SQUARE_SIZE))
        if self.selected_pos:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (self.selected_pos[0] * SQUARE_SIZE, self.selected_pos[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
            for move in self.valid_moves:
                pygame.draw.circle(screen, (0, 255, 0), (move[0] * SQUARE_SIZE + SQUARE_SIZE // 2, move[1] * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 4)
        # Turn indicator
        turn_indicator_pos = (BOARD_WIDTH, 10)  # Adjust if needed for the actual position
        turn_text = f"Turn: {self.current_turn.capitalize()}"
        font = pygame.font.SysFont("Arial", 24)
        text_surface = font.render(turn_text, True, BLACK)
        screen.blit(text_surface, turn_indicator_pos)


    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
