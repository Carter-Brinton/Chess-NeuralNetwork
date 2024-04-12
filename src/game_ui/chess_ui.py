# chess_ui.py
import chess
import pygame
from constants.constants import *
from game_ui.chess_graph_and_plots_ui import ChessGraphAndPlotsUI
from game_ui.chess_misc_ui import ChessMiscUI
from game_ui.chess_move_tracking import ChessMoveTrackingUI
from game_ui.chess_play_ai_ui import ChessPlayAIUI
from game_ui.chess_promotion_ui import ChessPromotionUI
from game_ui.chess_restart_quit_ui import ChessRestartQuitUI
from game_ui.chess_select_color_ui import ChessSelectColorUI
from game_ui.chess_start_game_ui import ChessStartGameUI
from game_ui.chess_train_ai_ui import ChessTrainAIUI
from game_ui.chess_training_stats_ui import ChessTrainingStatsUI

class ChessUI:
    def __init__(self, screen, my_chess_board, board):
        self.screen = screen
        self.my_chess_board = my_chess_board
        self.board = board
        self.scroll_offset = 0  
        self.cancel_promotion = False

        self.MiscUI = ChessMiscUI(self)
        self.ChessMoveTrackingUI = ChessMoveTrackingUI(self)
        self.ChessPromotionUI = ChessPromotionUI(self)
        self.ChessRestartQuitUI = ChessRestartQuitUI(self)
        self.ChessSelectColorUI = ChessSelectColorUI(self)
        self.ChessStartGameUI = ChessStartGameUI(self)
        self.ChessTrainAIUI = ChessTrainAIUI(self)
        self.ChessPlayAIUI = ChessPlayAIUI(self)
        self.ChessGraphAndPlotsUI = ChessGraphAndPlotsUI(self)
        self.ChessTrainingStatsUI = ChessTrainingStatsUI(self)

    # MiscUI methods
    def draw_overlay(self):
        self.MiscUI.draw_overlay()
    def draw_gradient_left_to_right(self, rect, start_color, end_color):
        self.MiscUI.draw_gradient_left_to_right(rect, start_color, end_color)
    def draw_gradient_text(self, text, font, rect, start_color, end_color):
        self.MiscUI.draw_gradient_text(text, font, rect, start_color, end_color)

    # ChessMoveTrackingUI methods
    def draw_forward_and_back_ui(self, ui_x_start, ui_y_start):
        self.ChessMoveTrackingUI.draw_forward_and_back_ui(ui_x_start, ui_y_start)
    def draw_move_tracking_ui(self):
        self.ChessMoveTrackingUI.draw_move_tracking_ui()

    # ChessPromotionUI methods
    def draw_promotion_ui(self, pawn_square, player_color):
        return self.ChessPromotionUI.draw_promotion_ui(pawn_square, player_color)

    # ChessRestartQuitUI methods
    def draw_restart_game_button(self, ui_x_start, ui_y_start, ui_height):
        self.ChessRestartQuitUI.draw_restart_game_button(ui_x_start, ui_y_start, ui_height)

    # ChessSelectColorUI methods
    def draw_select_starting_color_ui(self):
        self.ChessSelectColorUI.draw_select_starting_color_ui()

    # ChessStartGameUI methods
    def draw_start_game_popup(self):
        self.ChessStartGameUI.draw_start_game_popup()

    # ChessTrainAIUI methods
    def draw_train_ai_popup(self):
        self.ChessTrainAIUI.draw_train_ai_popup()

    # ChessPlayAIUI methods
    def draw_play_ai_popup(self):
        self.ChessPlayAIUI.draw_play_ai_popup()
    
    # ChessGraphAndPlotsUI methods
    def update_graph_and_plots_ui(self, episode_rewards_white, episode_rewards_black, episode_losses, epsilon_values):
        self.ChessGraphAndPlotsUI.update_graph_and_plots_ui(episode_rewards_white, episode_rewards_black, episode_losses, epsilon_values)

    def visualize_neural_network(self):
        self.ChessGraphAndPlotsUI.visualize_neural_network()
    
    def plot_episode_rewards(self, episode_rewards_white, episode_rewards_black, episode_losses, epsilon_values):
        self.ChessGraphAndPlotsUI.plot_episode_rewards(episode_rewards_white, episode_rewards_black, episode_losses, epsilon_values)

    # ChessTrainingStatsUI methods
    def draw_training_stats(self):
        self.ChessTrainingStatsUI.draw_training_stats()