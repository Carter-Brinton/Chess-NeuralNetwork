# load_images.py
import pygame
from constants.constants import *

def load_images():
    pieces = ['Pawn', 'Knight', 'Bishop', 'Rook', 'Queen', 'King']
    images = {}
    for piece in pieces:
        for color in ['White', 'Black']:
            key = color[0].upper() + piece
            images[key] = pygame.transform.scale(pygame.image.load(f"./src/assets/images/chess_pieces/{color.lower()}-{piece.lower()}.png"), (SQUARE_SIZE, SQUARE_SIZE))
    return images
