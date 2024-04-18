import pygame
import sys
from pygame.locals import *
from utility import *
from utility.entities import *

class MainMenu:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.font = pygame.font.Font(None, 36)
        self.menu_options = ["Start Game", "Quit"]
        self.selected_option = 0

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.menu_options)
        elif keys[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.menu_options)
        elif keys[pygame.K_RETURN]:
            if self.selected_option == 0:
                self.gameStateManager.set_state('start')
            elif self.selected_option == 1:
                pygame.quit()
                sys.exit()

    def draw_menu(self):
        self.display.fill(WHITE)
        for i, option in enumerate(self.menu_options):
            color = RED if i == self.selected_option else BLACK
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
            self.display.blit(text, text_rect)

    def run(self):
        self.handle_events()
        self.draw_menu()