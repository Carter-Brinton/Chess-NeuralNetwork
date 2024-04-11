import chess
import pygame
from constants.constants import *

class ChessTrainAIUI:
    def __init__(self, chess_ui):
        self.chess_ui = chess_ui
        # Define initial UI states
        self.num_episodes = 1000
        self.visualize_training_options = ["Yes", "No"]
        self.visualize_training_selection = 0  # 0 for "Yes", 1 for "No"
        self.train_from_scratch_options = ["New Model", "Partial Model", "Latest Model"]
        self.train_from_scratch_selection = 0  # Index in the options list
        self.popup_width = 400
        self.popup_height = 400
        self.popup_x = (WINDOW_WIDTH - self.popup_width) // 2
        self.popup_y = (WINDOW_HEIGHT - self.popup_height) // 2
        self.options_font = pygame.font.Font(None, 30)
        self.start_cancel_font = pygame.font.Font(None, 24)

        # Define the rects for the "Visualize Training" radio buttons
        self.visualize_training_rects = [
            pygame.Rect(self.popup_x + 250 + i * 60, self.popup_y + 110, 50, 30) for i in range(2)
        ]
        
        # Define the rect for the "Starting Point" dropdown
        self.starting_point_rect = pygame.Rect(self.popup_x + 250, self.popup_y + 170, 130, 30)
        
        # Define the rect for the "Start Training" and "Cancel" button
        self.start_training_button_rect = pygame.Rect(self.popup_x + 35, self.popup_y + 340, 140, 40)
        self.cancel_training_button_rect = pygame.Rect(self.popup_x + 225, self.popup_y + 340, 140, 40)

        # Define dropdown properties for "Number of Episodes"
        self.num_episodes_options = ["100", "500", "1000"]
        self.num_episodes_rect = pygame.Rect(self.popup_x + 250, self.popup_y + 50, 100, 30)
        self.num_episodes_selected_index = 0

    def draw_train_ai_popup(self):
        self.chess_ui.draw_overlay()

        pygame.draw.rect(self.chess_ui.screen, GREY, (self.popup_x, self.popup_y, self.popup_width, self.popup_height))

        texts = ["Number of Episodes:", "Visualize Training:", "Starting Point:"]
        base_y_offset = 50
        y_gap = 60

        # Draw static texts
        for i, text in enumerate(texts):
            text_surface = self.options_font.render(text, True, BLACK)
            self.chess_ui.screen.blit(text_surface, (self.popup_x + 20, self.popup_y + base_y_offset + i * y_gap))

        # Draw input box for "Number of Episodes"
        pygame.draw.rect(self.chess_ui.screen, WHITE, self.num_episodes_rect, 2)
        num_episodes_text = self.options_font.render(self.num_episodes_options[self.num_episodes_selected_index], True, BLACK)
        self.chess_ui.screen.blit(num_episodes_text, (self.num_episodes_rect.x + 5, self.num_episodes_rect.y + 5))

        # Draw radio buttons for "Visualize Training"
        for i, option in enumerate(self.visualize_training_options):
            rect = self.visualize_training_rects[i]
            pygame.draw.rect(self.chess_ui.screen, WHITE, rect)
            option_text = self.options_font.render(option, True, BLACK)
            self.chess_ui.screen.blit(option_text, (rect.x + 5, rect.y + 5))
            if i == self.visualize_training_selection:
                pygame.draw.rect(self.chess_ui.screen, BLUE, rect, 2)

        # Draw dropdown for "Starting Point"
        pygame.draw.rect(self.chess_ui.screen, WHITE, self.starting_point_rect)
        selected_option_text = self.start_cancel_font.render(self.train_from_scratch_options[self.train_from_scratch_selection], True, BLACK)
        self.chess_ui.screen.blit(selected_option_text, (self.starting_point_rect.x + 5, self.starting_point_rect.y + 5))

        # Draw the "Start Training" button
        pygame.draw.rect(self.chess_ui.screen, PALEBLUE, self.start_training_button_rect)
        start_training_text = self.start_cancel_font.render("Start Training", True, BLACK)
        text_pos = self.start_training_button_rect.x + (self.start_training_button_rect.width - start_training_text.get_width()) // 2, \
                   self.start_training_button_rect.y + (self.start_training_button_rect.height - start_training_text.get_height()) // 2
        self.chess_ui.screen.blit(start_training_text, text_pos)

        pygame.draw.rect(self.chess_ui.screen, PALERED, self.cancel_training_button_rect)
        cancel_training_text = self.start_cancel_font.render("Cancel Training", True, BLACK)
        text_pos = self.cancel_training_button_rect.x + (self.start_training_button_rect.width - cancel_training_text.get_width()) // 2, \
                   self.cancel_training_button_rect.y + (self.cancel_training_button_rect.height - cancel_training_text.get_height()) // 2
        self.chess_ui.screen.blit(cancel_training_text, text_pos)

    def handle_clicks(self, pos):
        # Handling clicks for "Number of Episodes" dropdown
        if self.num_episodes_rect.collidepoint(pos):
            self.num_episodes_selected_index = (self.num_episodes_selected_index + 1) % len(self.num_episodes_options)
            return

        # Handling clicks for "Visualize Training" radio buttons
        for i, rect in enumerate(self.visualize_training_rects):
            if rect.collidepoint(pos):
                self.visualize_training_selection = i
                return

        # Handling clicks for "Train from Scratch" dropdown
        if self.starting_point_rect.collidepoint(pos):
            self.train_from_scratch_selection = (self.train_from_scratch_selection + 1) % len(self.train_from_scratch_options)
            return
