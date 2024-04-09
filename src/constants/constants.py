# constants.py
import pygame

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
