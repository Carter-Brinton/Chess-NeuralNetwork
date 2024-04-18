# chess_training_environment.py
from neural_network.dqn_agent import DQNAgent
import numpy as np
import chess
import random
import torch
import copy
import queue
import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Adjust these parameters as needed
BATCH_SIZE = 32 # Influences how many experiences (state, action, reward, next state) the DQN agent will use to learn in one replay step
STATE_SIZE = 14 * 8 * 8  # Example state size based on the board_to_tensor representation
ACTION_SIZE = 4096  # Assuming a simplification where every square to every square is a potential move
MAX_EPISODES = 1000

class ChessTrainingEnvironment:
    def __init__(self, board, my_chess_board, my_chess_ui):
        self.board = board
        self.my_chess_board = my_chess_board
        self.my_chess_ui = my_chess_ui
        self.agent = DQNAgent(STATE_SIZE, ACTION_SIZE)  # Initialize the DQN agent here
        self.ai_training_finished = False
        self.stop_ai = False
        self.move_counter = 0
        self.white_agent = copy.deepcopy(self.agent)  # Create a separate agent for white
        self.black_agent = copy.deepcopy(self.agent)  # Create a separate agent for black
        self.update_queue = queue.Queue()  # Thread-safe queue for UI updates

        # Metrics storage
        self.episode_rewards_white = []
        self.episode_rewards_black = []
        self.episode_losses = []
        self.epsilon_values = []

    def start_playing_against_ai(self):
        # Reset move counter at the start of each game
        self.move_counter = 0
        while not self.board.is_game_over():
            if self.stop_ai:
                self.stop_ai = False
                break
            if self.my_chess_board.is_ai_turn:
                move = self.get_random_legal_move()
                if move:
                    logging.info(f"AI making move: {move.uci()}")
                    self.board.push(move)
                    self.my_chess_board.make_ai_vs_player_move(move.uci())
                    self.move_counter += 1  # Increment move counter
                else:
                    self.ai_training_finished = True
                    break
   
    def start_training_ai(self):
        episode = 1
        while not self.ai_training_finished and episode <= MAX_EPISODES and not self.stop_ai:
            self.stop_ai = False
            
            self.board.reset()
            state = self.board_to_tensor(self.board)
            self.move_counter = 0
            total_reward_white = 0
            total_reward_black = 0
            episode_loss = 0

            while not self.board.is_game_over() and not self.stop_ai:
                current_agent = self.white_agent if self.board.turn == chess.WHITE else self.black_agent
                move, action = self.get_nn_move(current_agent)
                if move:
                    self.board.push(move)
                    next_state = self.board_to_tensor(self.board)
                    reward = self.score_move(move)
                    done = self.board.is_game_over()
                    self.move_counter += 1

                    current_agent.remember(state, action, reward, next_state, done)
                    state = next_state

                    if len(current_agent.memory) > BATCH_SIZE:
                        loss = current_agent.replay(BATCH_SIZE)
                        episode_loss += loss  # Collect loss for plotting
                    
                    # Log details about the move and who made it
                    logging.info(f"Turn: {'White' if self.board.turn == chess.BLACK else 'Black'}, Move: {move.uci()}, Reward: {reward}, NN Move: {action is not None}")

                    if self.board.turn == chess.WHITE:
                        total_reward_black += reward
                    else:
                        total_reward_white += reward
                    logging.info(f"Current White Score = {total_reward_white}, Current Black Score = {total_reward_black}\n")

                    # Post an update to the queue ( gets called from chess_game (commented out))
                    self.update_queue.put((total_reward_white, total_reward_black, episode_loss, current_agent.epsilon))
                    # self.my_chess_ui.draw_training_stats(episode, total_reward_white, total_reward_black, episode_loss, current_agent.epsilon)

                else:
                    logging.error("Invalid move selected by NN or no moves available.")
                    break

            logging.info(f"Episode {episode} complete: White Score = {total_reward_white}, Black Score = {total_reward_black}, Total Moves = {self.move_counter}")

            episode += 1
            if episode > MAX_EPISODES:
                self.ai_training_finished = True


    def process_updates(self):
        try:
            while not self.update_queue.empty():
                total_reward_white, total_reward_black, episode_loss, epsilon = self.update_queue.get_nowait()
                # Assume function to update graph and plots
                self.my_chess_ui.update_graph_and_plots_ui(
                    total_reward_white, total_reward_black, episode_loss, epsilon)
        except queue.Empty:
            pass

    def score_move(self, move):
        reward = 0
        if self.board.is_capture(move):
            captured_piece = self.board.piece_at(move.to_square)
            piece_value = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
            reward += piece_value.get(captured_piece.symbol().upper(), 0)
        
        # Additional rewards/penalties could be added here based on strategic positions etc.

        return reward


    def get_random_legal_move(self):
        legal_moves = list(self.board.legal_moves)
        return random.choice(legal_moves) if legal_moves else None
    
    def get_nn_move(self, agent):
        board_tensor = self.board_to_tensor(self.board)
        if random.random() > agent.epsilon:  # Ensure that NN moves are logged
            with torch.no_grad():
                action_values = agent.model(board_tensor)
                action = torch.argmax(action_values).item()
                move = self.action_to_move(action)
                if move and move in self.board.legal_moves:
                    logging.info("NN was used for this move.")
                    return move, action
        else:
            logging.info("Random move due to high epsilon.")
            return self.get_random_legal_move(), None



    def action_to_move(self, action):
        legal_moves = list(self.board.legal_moves)
        # Map the action to a move only if it's within the bounds of legal moves
        if legal_moves:
            index = action % len(legal_moves)  # Use modulo to wrap around the list
            return legal_moves[index]
        return None


    def step(self, action):
        # Directly use the action to find the move
        move = self.action_to_move(action)
        if move:
            self.board.push(move)
            next_state = self.board_to_tensor(self.board)
            reward = self.score_move(self.board.result())
            done = self.board.is_game_over()
            return next_state, reward, done
        else:
            # Penalize illegal moves or handle no move
            return None, -1, True


    def board_to_tensor(self, board):
        # Initialize a zero tensor with shape [14, 8, 8] for 12 piece types + 2 for special states
        board_tensor = torch.zeros(14, 8, 8)
        piece_to_channel = {
            'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,  # White pieces
            'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11 # Black pieces
        }

        # Populate the tensor with piece positions
        for i in range(64):
            piece = board.piece_at(i)
            if piece:
                channel = piece_to_channel.get(piece.symbol())
                row, col = divmod(i, 8)
                board_tensor[channel, row, col] = 1

        # Castling rights (optionally handled based on your approach)
        # Add other special states as needed

        # Finally, add the batch dimension
        return board_tensor.unsqueeze(0)  # Correctly adds the batch dimension, resulting in [1, 14, 8, 8]
