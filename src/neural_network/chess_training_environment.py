# chess_training_environment.py
import numpy as np
import chess
import random

class ChessTrainingEnvironment:
    def __init__(self, board, my_chess_board):
        self.board = board
        self.my_chess_board = my_chess_board
        self.ai_training_finished = False
        self.stop_ai = False

    def start_training_ai(self):
        while not self.board.is_game_over():
            if(self.stop_ai):
                self.stop_ai = False
                break
            move = self.get_random_legal_move()
            if move:
                self.board.push(move)
                self.my_chess_board.make_ai_vs_ai_move(move.uci())
            else:
                self.ai_training_finished = True
                break 
    
    def start_playing_against_ai(self):
        while not self.board.is_game_over():
            if(self.stop_ai):
                self.stop_ai = False
                break
            if(self.my_chess_board.is_ai_turn):
                move = self.get_random_legal_move()
                if move:
                    self.board.push(move)
                    self.my_chess_board.make_ai_vs_player_move(move.uci())
                else:
                    self.ai_training_finished = True
                    break 

    def get_random_legal_move(self):
        legal_moves = list(self.board.legal_moves)
        return random.choice(legal_moves) if legal_moves else None
