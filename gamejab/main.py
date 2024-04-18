import pygame
import sys
from pygame.locals import *
from utility import *
from utility.entities import *


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.player = Player(self.screen)
        self.npc = NPC(self.screen)
        self.door = Door()

        self.gameStateManager = GameStateManager('start')
        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(self.screen, self.gameStateManager)

        self.states = {'start': self.start, 'level': self.level}
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Move the player
            self.player.move()

            # Draw the background
            self.screen.fill(WHITE)  # Fill the screen with white
            self.screen.blit(background_image, (0,0))

            # Check if the player has crossed the right border to change the scene
            if self.gameStateManager.get_state() == 'start':
                if self.player.rect.colliderect(self.door.rect):
                    self.gameStateManager.set_state('level')
                    self.player.rect.left = 0
                

            self.states[self.gameStateManager.get_state()].run()
            
            self.screen.blit(self.player.image, self.player.rect)
            # Render NPC only when the state is "start"
            if self.gameStateManager.get_state() == 'start':
                self.screen.blit(self.npc.image, self.npc.rect)
                self.npc.update(self.player, self.screen)
                self.screen.blit(self.door.image, self.door.rect)

            pygame.display.update()
            self.clock.tick(FPS)


class Level:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        self.display.fill('BLUE')


class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.background_image = background_image
    def run(self):
        self.display.blit(self.background_image, (0,0))
        

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
