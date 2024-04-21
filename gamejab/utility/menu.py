import pygame
import sys
from pygame.locals import *
from utility import *
from utility.entities import *

class MainMenu:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.font = pygame.font.Font('gamejab/materials/fonts/font.TTF', 50)
        self.menu_options = ["Start Game", "Quit", "Controls"]
        self.selected_option = 0
        self.key_pressed = False  # Variable to track key press state

    def handle_events(self):
        keys = pygame.key.get_pressed()
        
        if not self.key_pressed:  # Check if a key is not already pressed
            if keys[pygame.K_UP]:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                self.key_pressed = True  # Set key press state to True
            elif keys[pygame.K_DOWN]:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                self.key_pressed = True  # Set key press state to True
            elif keys[pygame.K_RETURN]:
                if self.selected_option == 0:
                    self.gameStateManager.set_state('start')
                elif self.selected_option == 1:
                    pygame.quit()
                    sys.exit()
                elif self.selected_option == 2:
                    self.gameStateManager.set_state('controls')
                self.key_pressed = True  # Set key press state to True
        
        # Reset key press state if no keys are pressed
        if not any(keys):
            self.key_pressed = False

    def draw_menu(self):
    # Load the background image
        background_image = pygame.image.load('gamejab/materials/images/menu1.png').convert()
    # Scale the background image to fit the display size
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    # Blit the background image onto the display
        self.display.blit(background_image, (0, 0))
    
    # Draw menu options on top of the background image
        for i, option in enumerate(self.menu_options):
            color = RED if i == self.selected_option else BLACK
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
            self.display.blit(text, text_rect)

    def draw_controls(self):
        self.display.fill(WHITE)
        control_text = [
            "Controls:",
            "E: Interact with objects",
            "SPACEBAR: Interact with NPCs",
            "ENTER: Choose an option",
            "Arrows: Walk",
            "Press ESC to return to main menu"
        ]
        control_font = pygame.font.Font(None, 30)
        for i, line in enumerate(control_text):
            text = control_font.render(line, True, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 30))
            self.display.blit(text, text_rect)

    def run(self):
        if self.gameStateManager.get_state() == 'main_menu':
            self.handle_events()
            self.draw_menu()
        elif self.gameStateManager.get_state() == 'controls':
            self.draw_controls()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.gameStateManager.set_state('main_menu')
