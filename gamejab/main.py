import pygame
import sys
from pygame.locals import *
from utility import *
from utility.entities import *
from utility.menu import *



class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.player = Player(self.screen)
        self.npc = NPC(self.screen)

        self.gameStateManager = GameStateManager('main_menu')
        self.main_menu = MainMenu(self.screen, self.gameStateManager)
        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(self.screen, self.gameStateManager)

        self.states = {'main_menu': self.main_menu, 'start': self.start, 'level': self.level}

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.gameStateManager.get_state() == 'main_menu':
                self.main_menu.run()
            else:
                # Move the player
                self.player.move()

                # Draw the background
                self.screen.fill(WHITE)  # Fill the screen with white

                # Check if the player has crossed the right border to change the scene
                if self.gameStateManager.get_state() == 'start':
                    if self.player.rect.colliderect(self.start.door.rect):
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_e]:
                            self.gameStateManager.set_state('level')
                            self.player.rect.left = 0

                if self.gameStateManager.get_state() == 'level':
                    if self.player.rect.colliderect(self.level.door.rect):
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_e]:
                            self.gameStateManager.set_state('start')
                            self.player.rect.right = WIDTH

                self.states[self.gameStateManager.get_state()].run()

                self.screen.blit(self.player.image, self.player.rect)
                # Render NPC only when the state is "start"
                if self.gameStateManager.get_state() == 'start':
                    self.screen.blit(self.npc.image, self.npc.rect)
                    self.npc.update(self.player, self.screen)

            pygame.display.update()
            self.clock.tick(FPS)

class Level:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.door = Door()  # Add a Door object to the level
        
        # Position the door at the middle left border
        self.door.rect.right = 50
        self.door.rect.centery = HEIGHT // 2

    def run(self):
        self.display.fill('BLUE')
        self.display.blit(self.door.image, self.door.rect)  


class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.background_image = background_image
        self.door = Door()  # Add a Door object to the start level
        
        # Position the door at the middle left border
        self.door.rect.left = WIDTH - 50
        self.door.rect.centery = 300

    def run(self):
        self.display.blit(self.background_image, (0,0))
        self.display.blit(self.door.image, self.door.rect)
        

class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state



if __name__ == '__main__':
    game = Game()
    game.run()
