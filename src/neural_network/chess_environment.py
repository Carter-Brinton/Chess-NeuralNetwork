import numpy as np
import chess

class ChessEnvironment:
    def __init__(self, game):
        self.game = game
        self.board = game.board

    def reset(self):
        """
        Resets the chess board to the initial state.
        Returns the initial state.
        """
        self.board.reset()
        return self._get_observation()

    def step(self, action):
        """
        Executes the given action (move) in the environment.
        Returns the next state, reward, and done status.
        """
        move = self._action_to_move(action)
        reward = 0
        done = False
        
        # Check if the move is legal before making it
        if move in self.board.legal_moves:
            self.board.push(move)
            reward = self._get_reward()
            done = self.board.is_game_over()
        else:
            reward = -1  # Penalize illegal moves
        
        next_state = self._get_observation()
        return next_state, reward, done

    def _get_observation(self):
        """
        Converts the current board state into a neural network-friendly format.
        """
        # Placeholder for your state representation logic
        # For simplicity, this could be a flattened array representing the board
        observation = np.zeros((64,), dtype=int)
        for i in range(64):
            piece = self.board.piece_at(i)
            if piece:
                # Assign unique integers to each piece type and color
                observation[i] = {'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
                                  'p': -1, 'n': -2, 'b': -3, 'r': -4, 'q': -5, 'k': -6}.get(piece.symbol(), 0)
        return observation

    def _action_to_move(self, action):
        """
        Converts an action (typically an integer) to a chess move.
        Placeholder for converting action integers to chess.Move objects.
        """
        # Example conversion, needs to be aligned with your action representation
        move = chess.Move.from_uci(action)
        return move

    def _get_reward(self):
        """
        Calculate the reward after the last move.
        Placeholder for reward calculation logic.
        """
        # Example simple reward system - customize as needed
        if self.board.is_checkmate():
            return 100  # Reward for winning
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            return -50  # Penalty for draw
        else:
            return 0  # No reward for other moves
