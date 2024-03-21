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
        grid_x, grid_y = x // SQUARE_SIZE, y // SQUARE_SIZE  # Convert mouse coordinates to board grid

        # Deselect piece if clicked outside the board or on the same piece
        if grid_x >= BOARD_SIZE or grid_y >= BOARD_SIZE or (self.selected_pos == (grid_x, grid_y)):
            self.selected_piece = None
            self.selected_pos = None
            self.valid_moves = []
            return False

        # If a piece is already selected
        if self.selected_piece:
            # Move the piece if a valid destination is selected
            if (grid_x, grid_y) in self.valid_moves:
                self.board[self.selected_pos[1]][self.selected_pos[0]] = None
                self.board[grid_y][grid_x] = self.selected_piece
                self.switch_turn()  # Switch turns after a successful move
                self.selected_piece = None
                self.selected_pos = None
                self.valid_moves = []
                return True
            else:
                # Deselect if an invalid move was attempted
                self.selected_piece = None
                self.selected_pos = None
                self.valid_moves = []
                return False
        else:
            # Select a piece if none is selected and it matches the current turn
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
        screen.fill(WHITE)
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
