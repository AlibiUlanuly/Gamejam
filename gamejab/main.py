import pygame
import sys
from pygame.locals import *
from utility import *
from utility.entities import *
from utility.menu import *
from utility.objects import *
from utility.questions import questions_quiz
import random

class GameOverScreen:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.font_title = pygame.font.Font('gamejab/materials/fonts/Font2.ttf', 60)
        self.font_desc = pygame.font.Font('gamejab/materials/fonts/Font2.ttf', 30)
        self.title = "Game Over"
        self.description = "Don't miss your endterms..."
        self.key_pressed = False  # Variable to track key press state

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if not self.key_pressed and keys[pygame.K_RETURN]:
            self.gameStateManager.set_state('main_menu')
            self.key_pressed = True
        
        if not any(keys):
            self.key_pressed = False

    def draw(self):
        self.display.fill((0, 0, 0))  # Darken the screen
        title_text = self.font_title.render(self.title, True, WHITE)
        desc_text = self.font_desc.render(self.description, True, WHITE)
        
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        desc_rect = desc_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        
        self.display.blit(title_text, title_rect)
        self.display.blit(desc_text, desc_rect)

    def run(self):
        self.handle_events()
        self.draw()


class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('gamejab/materials/sounds/music.mp3')
        pygame.mixer.music.play(-1)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
 
        self.event1 = Event1()
        self.event2 = Event2()
        self.event3 = Event3()
        self.event4 = Event4()
        self.event5 = Event5()
        self.event6 = Event6()
        
        self.correct_answers_count = 0
        self.questions = questions_quiz
        self.quiz_started = False
        self.quiz_box = QuizBox(self.screen, self.questions, self.event4)

        self.player = Player(self.screen)
        self.npc = NPC(self.screen, self.event1, self.event2, self.event3, self.questions, self.event5)
        self.npc2 = NPC2(self.screen, self.event6)
        self.gameStateManager = GameStateManager('main_menu')
        self.main_menu = MainMenu(self.screen, self.gameStateManager)
        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(self.screen, self.gameStateManager)
        self.level2 = Level2(self.screen, self.gameStateManager, self.event5, self.player, self.npc2)
        self.game_over_screen = GameOverScreen(self.screen, self.gameStateManager)

        self.states = {'main_menu': self.main_menu, 'start': self.start, 'level': self.level, 'level2': self.level2, 'game_over': self.game_over_screen}

    def start_quiz(self):
        self.quiz_started = True

    def handle_quiz_events(self, event):
        if self.quiz_started:
            self.quiz_box.handle_input(event)


    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.quiz_started:
                    self.handle_quiz_events(event)
            if self.gameStateManager.get_state() == 'main_menu':
                self.main_menu.run()
            elif self.gameStateManager.get_state() == 'game_over':
                self.game_over_screen.run()
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
                            pygame.mixer.Sound('gamejab/materials/sounds/dooropen.mp3').play()
                            self.gameStateManager.set_state('level')
                            self.player.rect.left = 0
                if self.event3.completed and not self.quiz_started:
                    self.start_quiz()
                    
                if self.gameStateManager.get_state() == 'level':
                    self.level.display.blit(self.level.background_image, (0,0))
                    self.level.display.blit(self.level.door.image, self.level.door.rect)  
                    self.level.display.blit(self.level.door2.image, self.level.door2.rect)
                    if self.player.rect.colliderect(self.level.door.rect):
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_e]:
                            pygame.mixer.Sound('gamejab/materials/sounds/dooropen.mp3').play()
                            self.gameStateManager.set_state('start')
                            self.player.rect.right = WIDTH
                    elif self.player.rect.colliderect(self.level.door2.rect):
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_e]:
                            pygame.mixer.Sound('gamejab/materials/sounds/dooropen.mp3').play()
                            self.gameStateManager.set_state('level2')
                            self.player.rect.left = 0
                    if self.event1.completed:
                        if self.level.adapter is not None:  # Check if adapter exists
                            self.level.display.blit(self.level.adapter.image, self.level.adapter.rect)
                            if self.player.rect.colliderect(self.level.adapter.rect):
                                keys = pygame.key.get_pressed()
                                if keys[pygame.K_e]:
                                    pygame.mixer.Sound('gamejab/materials/sounds/collected.mp3').play()
                                    self.level.adapter = None
                                    self.event2.completed = True       
                
                if self.gameStateManager.get_state() == 'level2':
                    if self.player.rect.colliderect(self.level2.door.rect):
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_e]:
                            pygame.mixer.Sound('gamejab/materials/sounds/dooropen.mp3').play()
                            self.gameStateManager.set_state('level')
                            self.player.rect.right = WIDTH

                self.states[self.gameStateManager.get_state()].run()
                self.correct_answers_count = self.quiz_box.correct_answers
                if self.event4.completed:
                    self.quiz_started = False
                    if self.correct_answers_count == 3:
                        self.event5.completed = True
                self.screen.blit(self.player.image, self.player.rect)
                # Render NPC only when the state is "start"
                if self.gameStateManager.get_state() == 'start':
                    self.screen.blit(self.npc.image, self.npc.rect)
                    self.npc.update(self.player, self.screen)
                if self.quiz_started and self.event3.completed:
                    self.quiz_box.update()
                if self.event6.completed == True:
                    self.gameStateManager.set_state('game_over')
            pygame.display.update()
            self.clock.tick(FPS)

class Level:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.background_image = background_image2
        self.door = Door(20, HEIGHT // 2)  # Add a Door object to the level
        self.door2 = Door(WIDTH - 10, HEIGHT // 2)
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
    def __init__ (self, display, gameStateManager, event5, player, npc):
        self.display = display
        self.background_image3 = background_image3
        self.gameStateManager = gameStateManager
        self.event5 = event5
        self.player = player
        self.npc2 = npc
        self.door = Door(5, HEIGHT // 3)
    def run(self):
        self.display.blit(self.background_image3, (0, 0))
        self.display.blit(self.door.image, self.door.rect)
        if self.event5.completed:
            self.display.blit(self.npc2.image, self.npc2.rect)
            self.npc2.update(self.player, self.display)

        

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

class Event5:
    def __init__(self):
        self.completed = False

class Event6:
    def __init__(self):
        self.completed = False


if __name__ == '__main__':
    game = Game()
    game.run()