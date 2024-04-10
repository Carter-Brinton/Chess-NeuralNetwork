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
        self.train_from_scratch_options = ["New Model", "Medium Model", "Latest Model"]
        self.train_from_scratch_selection = 0  # Index in the options list
        self.popup_width = 400
        self.popup_height = 400
        self.popup_x = (WINDOW_WIDTH - self.popup_width) // 2
        self.popup_y = (WINDOW_HEIGHT - self.popup_height) // 2
        self.font = pygame.font.Font(None, 30)

        # Define the rects for the "Visualize Training" radio buttons
        self.visualize_training_rects = [
            pygame.Rect(self.popup_x + 250 + i * 60, self.popup_y + 110, 50, 30) for i in range(2)
        ]
        
        # Define the rect for the "Train from Scratch" dropdown
        self.train_from_scratch_rect = pygame.Rect(self.popup_x + 250, self.popup_y + 170, 100, 30)
        
        # Define the rect for the "Start Training" button
        self.start_training_button_rect = pygame.Rect(self.popup_x + 100, self.popup_y + 340, 200, 40)

    def draw_train_ai_popup(self):
        self.chess_ui.draw_overlay()

        pygame.draw.rect(self.chess_ui.screen, GREY, (self.popup_x, self.popup_y, self.popup_width, self.popup_height))

        texts = ["Number of Episodes:", "Visualize Training:", "Starting Point:"]
        base_y_offset = 50
        y_gap = 60

        # Draw static texts
        for i, text in enumerate(texts):
            text_surface = self.font.render(text, True, BLACK)
            self.chess_ui.screen.blit(text_surface, (self.popup_x + 20, self.popup_y + base_y_offset + i * y_gap))

        # Draw input box for "Number of Episodes"
        episodes_input_rect = pygame.Rect(self.popup_x + 250, self.popup_y + base_y_offset, 100, 30)
        pygame.draw.rect(self.chess_ui.screen, WHITE, episodes_input_rect)

        # Draw radio buttons for "Visualize Training"
        for i, option in enumerate(self.visualize_training_options):
            rect = self.visualize_training_rects[i]
            pygame.draw.rect(self.chess_ui.screen, WHITE, rect)
            option_text = self.font.render(option, True, BLACK)
            self.chess_ui.screen.blit(option_text, (rect.x + 5, rect.y + 5))
            if i == self.visualize_training_selection:
                pygame.draw.circle(self.chess_ui.screen, BLUE, rect.center, 10)

        # Draw dropdown for "Train from Scratch"
        pygame.draw.rect(self.chess_ui.screen, WHITE, self.train_from_scratch_rect)
        selected_option_text = self.font.render(self.train_from_scratch_options[self.train_from_scratch_selection], True, BLACK)
        self.chess_ui.screen.blit(selected_option_text, (self.train_from_scratch_rect.x + 5, self.train_from_scratch_rect.y + 5))

        # Draw the "Start Training" button
        pygame.draw.rect(self.chess_ui.screen, PALEBLUE, self.start_training_button_rect)
        start_training_text = self.font.render("Start Training", True, BLACK)
        text_pos = self.start_training_button_rect.x + (self.start_training_button_rect.width - start_training_text.get_width()) // 2, \
                   self.start_training_button_rect.y + (self.start_training_button_rect.height - start_training_text.get_height()) // 2
        self.chess_ui.screen.blit(start_training_text, text_pos)

    def handle_clicks(self, pos):
        # Visualize Training radio buttons
        for i, rect in enumerate(self.visualize_training_rects):
            if rect.collidepoint(pos):
                self.visualize_training_selection = i
                return  # Stop checking after a hit

        # Train from Scratch dropdown
        if self.train_from_scratch_rect.collidepoint(pos):
            self.train_from_scratch_selection = (self.train_from_scratch_selection + 1) % len(self.train_from_scratch_options)
            return

        # Start Training button
        if self.start_training_button_rect.collidepoint(pos):
            # Placeholder for triggering the training logic
            print("Start Training button clicked")
            self.show_select_train_ai_popup = False  # Close the popup or start training
            return
