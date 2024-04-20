import pygame
import sys
from pygame.locals import *
from utility import *
from utility.entities import *
from utility.menu import *
from utility.objects import *
from utility import questions
import random

class Game():
    def __init__(self):
        pygame.init()
        self.event1 = Event1()
        self.event2 = Event2()
        self.event3 = Event3()
        self.questions = questions
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.player = Player(self.screen)
        self.npc = NPC(self.screen, self.event1, self.event2, self.event3, self.questions)

        self.gameStateManager = GameStateManager('main_menu')
        self.main_menu = MainMenu(self.screen, self.gameStateManager)
        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(self.screen, self.gameStateManager)
        self.level2 = Level2(self.screen, self.gameStateManager)

        self.states = {'main_menu': self.main_menu, 'start': self.start, 'level': self.level, 'level2': self.level2}

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
                    self.level.display.blit(self.level.background_image, (0,0))
                    self.level.display.blit(self.level.door.image, self.level.door.rect)  
                    self.level.display.blit(self.level.door2.image, self.level.door.rect)
                    if self.player.rect.colliderect(self.level.door.rect):
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_e]:
                            self.gameStateManager.set_state('start')
                            self.player.rect.right = WIDTH
                    elif self.player.rect.colliderect(self.level.door2.rect):
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_e]:
                            self.gameStateManager.set_state('level2')
                            self.player.rect.left = 0
                    if self.event1.completed:
                        if self.level.adapter is not None:  # Check if adapter exists
                            self.level.display.blit(self.level.adapter.image, self.level.adapter.rect)
                            if self.player.rect.colliderect(self.level.adapter.rect):
                                keys = pygame.key.get_pressed()
                                if keys[pygame.K_e]:
                                    self.level.adapter = None
                                    self.event2.completed = True       
                
                if self.gameStateManager.get_state() == 'level2':
                    if self.player.rect.colliderect(self.level2.door.rect):
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_e]:
                            self.gameStateManager.set_state('level')
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
        self.background_image = background_image2
        self.door = Door(50, HEIGHT // 2)  # Add a Door object to the level
        self.door2 = Door(WIDTH - 100, HEIGHT // 2)
        self.adapter = Adapter(random.randint(60, 600), random.randint(60, 600))
        # Position the door at the middle left border
    def run(self):
        pass


class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.background_image = background_image
        self.door = Door(WIDTH, 300)  # Add a Door object to the start level
        self.desk = Desk(180, 300)
        
        # Create and add a table object at the middle left border
        self.tables = []
        self.tables.append(Table(150, 500))
        self.tables.append(Table(150, 650))
        self.tables.append(Table(650, 500))
        self.tables.append(Table(650, 650))
        

    def run(self):
        self.display.blit(self.background_image, (0, 0))
        self.display.blit(self.door.image, self.door.rect)
        self.display.blit(self.desk.image, self.desk.rect)
        
        for table in self.tables:
            self.display.blit(table.image, table.rect)


class Level2:
    def __init__ (self, display, gameStateManager):
        self.display = display
        self.background_image3 = background_image3
        self.gameStateManager = gameStateManager
        self.door = Door(5, HEIGHT // 3)
    def run(self):
        self.display.blit(self.background_image3, (0, 0))
        self.display.blit(self.door.image, self.door.rect)

        

class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state

class Event1:
    def __init__(self):
        self.completed = False

class Event2:
    def __init__(self):
        self.completed = False

class Event3:
    def __init__(self):
        self.completed = False

class Event4:
    def __init__(self):
        self.completed = False


if __name__ == '__main__':
    game = Game()
    game.run()