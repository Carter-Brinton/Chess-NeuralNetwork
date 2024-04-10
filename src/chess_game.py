# chess_game.py
from constants.constants import *
from game_logic.chess_board import ChessBoard
from game_ui.chess_ui import ChessUI
from utils.load_images import load_images
import chess
import random
import numpy as np
from neural_network.chess_environment import ChessEnvironment
from neural_network.dqn_agent import DQNAgent

class ChessGame:
    def __init__(self, screen):
            self.board = chess.Board()
            self.screen = screen
            self.PIECES = load_images()
            self.offset_x, self.offset_y = OFFSET_X, OFFSET_Y
            self.player_color = random.choice([chess.WHITE, chess.BLACK])
            self.my_chess_board = ChessBoard(self.screen, self.PIECES, self.player_color, self.offset_x, self.offset_y, self.board)
            self.my_chess_ui = ChessUI(self.screen, self.my_chess_board, self.board)
            self.current_ui_state = None
            self.show_start_game_popup = True
            self.show_select_train_ai_popup = False
            self.show_select_play_ai_popup = False
            self.show_select_starting_color_popup = False

    def train_ai(episodes=1000):
        env = ChessEnvironment()
        state_size = env.state_size  # You need to define this based on your environment
        action_size = env.action_size  # Likewise, define based on your environment
        agent = DQNAgent(state_size, action_size)
        
        for e in range(episodes):
            state = env.reset()
            state = np.reshape(state, [1, state_size])
            for time in range(500):  # Maximum steps per episode
                action = agent.act(state)
                next_state, reward, done = env.step(action)
                next_state = np.reshape(next_state, [1, state_size])
                agent.remember(state, action, reward, next_state, done)
                state = next_state
                if done:
                    print(f"Episode: {e+1}/{episodes}, score: {time}, e: {agent.epsilon:.2}")
                    break
                if len(agent.memory) > 32:
                    agent.replay(32)
    
    # In ChessGame class
    def handle_start_game_clicks(self, pos):
        if self.show_start_game_popup:
            self.handle_start_game_popup_clicks(pos)
        elif self.show_select_train_ai_popup:
            self.handle_select_train_ai_clicks(pos)
        elif self.show_select_play_ai_popup:
            self.handle_select_play_ai_clicks(pos)
        elif self.show_select_starting_color_popup:
            self.handle_select_starting_color_clicks(pos)

    def handle_start_game_popup_clicks(self, pos):
        if self.my_chess_ui.ChessStartGameUI.start_train_button_rect.collidepoint(pos):
            self.show_select_train_ai_popup = True
            self.show_start_game_popup = False
            self.current_ui_state = 'train_ai'
        elif self.my_chess_ui.ChessStartGameUI.start_ai_button_rect.collidepoint(pos):
            self.show_select_starting_color_popup = True
            self.show_start_game_popup = False
            self.current_ui_state = 'play_ai'
        elif self.my_chess_ui.ChessStartGameUI.start_two_player_button_rect.collidepoint(pos):
            self.show_select_starting_color_popup = True
            self.show_start_game_popup = False
            self.current_ui_state = 'two_player'

# This method needs to be modified so the start button is pressed from here to disable the current ui state
    def handle_select_train_ai_clicks(self, pos):
        if self.current_ui_state == 'train_ai':
            self.my_chess_ui.ChessTrainAIUI.handle_clicks(pos)

    def handle_select_play_ai_clicks(self, pos):
        self.my_chess_ui.ChessPlayAIUI.handle_ai_level_click(pos)
        if self.my_chess_ui.chessSelectColorUI.white_button_rect.collidepoint(pos):
            self.player_color = chess.WHITE
            self.show_select_play_ai_popup = False
            self.current_ui_state = None
        elif self.my_chess_ui.chessSelectColorUI.black_button_rect.collidepoint(pos):
            self.player_color = chess.BLACK
            self.show_select_play_ai_popup = False
            self.current_ui_state = None
        elif self.my_chess_ui.chessSelectColorUI.random_button_rect.collidepoint(pos):
            self.show_select_play_ai_popup = False
            self.current_ui_state = None
            self.my_chess_board.update_player_color(random.choice([chess.WHITE, chess.BLACK]))

    def handle_select_starting_color_clicks(self, pos):
        if self.my_chess_ui.chessSelectColorUI.white_button_rect.collidepoint(pos):
            self.player_color = chess.WHITE
            self.show_select_starting_color_popup = False
            self.current_ui_state = None
            self.my_chess_board.update_player_color(chess.WHITE)
        elif self.my_chess_ui.chessSelectColorUI.black_button_rect.collidepoint(pos):
            self.player_color = chess.BLACK
            self.show_select_starting_color_popup = False
            self.current_ui_state = None
            self.my_chess_board.update_player_color(chess.BLACK)
        elif self.my_chess_ui.chessSelectColorUI.random_button_rect.collidepoint(pos):
            self.show_select_starting_color_popup = False
            self.current_ui_state = None
            self.my_chess_board.update_player_color(random.choice([chess.WHITE, chess.BLACK]))


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_start_game_clicks(event.pos)
                    if self.my_chess_ui.ChessRestartQuitUI.restart_button_rect.collidepoint(event.pos) and self.current_ui_state is None:
                        self.board.reset()
                        self.my_chess_board.reset()
                        self.show_start_game_popup = True
                    elif self.my_chess_ui.ChessRestartQuitUI.quit_button_rect.collidepoint(event.pos) and self.current_ui_state is None:
                        running = False
                    elif self.my_chess_board.awaiting_promotion:
                        # Handle promotion piece selection
                        for option_rect, promotion_piece in zip(self.my_chess_ui.ChessPromotionUI.promotion_option_buttons, [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]):
                            if option_rect.collidepoint(event.pos):
                                move = chess.Move(self.my_chess_board.selected_piece, self.my_chess_board.square_to_promote, promotion=promotion_piece)
                                if move in self.my_chess_board.legal_moves:
                                    self.board.push(move)
                                    self.my_chess_board.awaiting_promotion = False
                                    self.my_chess_board.selected_piece = None
                                    self.my_chess_board.legal_moves = list(self.board.legal_moves)
                                    self.my_chess_board.awaiting_promotion = False
                                    self.current_ui_state = None
                                    break
                        if self.my_chess_ui.ChessPromotionUI.cancel_promotion_button_rect.collidepoint(event.pos):
                            self.my_chess_board.awaiting_promotion = False
                            self.my_chess_board.selected_piece = None
                            self.my_chess_board.legal_moves = list(self.board.legal_moves)
                            self.my_chess_board.awaiting_promotion = False
                            self.current_ui_state = None
                    elif self.current_ui_state is None:
                        # Handle regular game interactions
                        pos = pygame.mouse.get_pos()
                        self.my_chess_board.handle_mouse_click(pos)
                    if self.my_chess_ui.ChessMoveTrackingUI.back_button_rect.collidepoint(event.pos) and self.current_ui_state is None:
                        self.my_chess_board.move_back()
                    elif self.my_chess_ui.ChessMoveTrackingUI.forward_button_rect.collidepoint(event.pos) and self.current_ui_state is None:
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
                self.current_ui_state = 'awaiting_promotion'
                self.my_chess_ui.draw_promotion_ui(None, self.board.piece_at(self.my_chess_board.selected_piece).color)

            if self.show_start_game_popup:
                self.current_ui_state = 'start_game'
                self.my_chess_ui.draw_start_game_popup()

            if self.show_select_train_ai_popup:
                self.my_chess_ui.draw_train_ai_popup()

            if self.show_select_starting_color_popup:
                self.my_chess_ui.draw_select_starting_color_ui()

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Chess Game')
    game = ChessGame(screen)
    game.run()