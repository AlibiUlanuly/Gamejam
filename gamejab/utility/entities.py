import pygame
from utility import *
from utility.dialogue import *

background1 = pygame.image.load('gamejab/materials/AnimatedStreet.png')
background_image = pygame.transform.scale(background1, (WIDTH, HEIGHT))
background2 = pygame.image.load('gamejab/materials/AnimatedStreet.png')

class NPC(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        original_image = pygame.image.load('gamejab/materials/Professor3.png')
        scaled_width = original_image.get_width() // 4
        scaled_height = original_image.get_height() // 4
        self.image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 100)

        self.font = pygame.font.SysFont(None, 24)
        self.dialogue_box = pygame.Surface((400, 150))  # Surface for the dialogue box
        self.dialogue_box.fill((200, 200, 200))
        self.dialogue_rect = self.dialogue_box.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        self.dialogue_lines = dialogue_script[:]  # Copy of the dialogue script
        self.current_line_index = 0  # Index of the current dialogue line
        self.screen = screen
        self.space_pressed = False  # Flag to indicate if spacebar is pressed
        self.show_next_line = False  # Flag to indicate if the next line should be shown

    def interact(self):
        self.space_pressed = True

    def update(self, player, screen):
        if pygame.sprite.collide_rect(self, player):
            self.interact()

        if self.space_pressed:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.show_next_line = True
            else:
                self.space_pressed = False

        if self.show_next_line and self.current_line_index < len(self.dialogue_lines):
            # Render the dialogue box
            self.screen.blit(self.dialogue_box, self.dialogue_rect)
            # Render the current dialogue line
            dialogue_surface = self.font.render(self.dialogue_lines[self.current_line_index], True, BLACK)
            dialogue_rect = dialogue_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            self.screen.blit(dialogue_surface, dialogue_rect)
            
            # Move to the next line
            self.current_line_index += 1
            self.show_next_line = False  # Reset flag

        # Reset index if all lines are shown
        if self.current_line_index >= len(self.dialogue_lines):
            self.current_line_index = 0







class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__() 
        self.walkFront = [pygame.image.load('gamejab/materials/walkfront1.png'), pygame.image.load('gamejab/materials/player-back.png'), pygame.image.load('gamejab/materials/walkfront2.png'), pygame.image.load('gamejab/materials/player-back.png')]
        self.walkDown = [pygame.image.load('gamejab/materials/walkdown1.png'), pygame.image.load('gamejab/materials/player-standing.png'), pygame.image.load('gamejab/materials/walkdown2.png'), pygame.image.load('gamejab/materials/player-standing.png')]
        self.walkRight = [pygame.image.load('gamejab/materials/walkright1.png'), pygame.image.load('gamejab/materials/player-right.png'), pygame.image.load('gamejab/materials/walkright2.png'), pygame.image.load('gamejab/materials/player-right.png')]
        self.walkLeft = [pygame.image.load('gamejab/materials/walkleft1.png'), pygame.image.load('gamejab/materials/player-left.png'), pygame.image.load('gamejab/materials/walkleft2.png'), pygame.image.load('gamejab/materials/player-left.png')]
        self.walkcount = 0
        self.image = pygame.image.load('gamejab/materials/player-standing.png')  # Load your player image here
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        
        self.screen = screen
        self.speed = VELOCITY

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        # Store the current position before moving
        current_x = self.rect.x
        current_y = self.rect.y

        # Move the player based on the pressed keys
        if pressed_keys[K_LEFT]:
            self.image = self.walkLeft[self.walkcount // 10 % len(self.walkLeft)]
            self.walkcount += 1
            self.rect.x -= self.speed
        if pressed_keys[K_RIGHT]:
            self.image = self.walkRight[self.walkcount // 10 % len(self.walkRight)]
            self.walkcount += 1
            self.rect.x += self.speed
        if pressed_keys[K_DOWN]:
            self.image = self.walkDown[self.walkcount // 10 % len(self.walkDown)]
            self.walkcount += 1
            self.rect.y += self.speed
        if pressed_keys[K_UP]:
            # Display walking animation for moving up
            self.image = self.walkFront[self.walkcount // 10 % len(self.walkFront)]
            self.walkcount += 1
            self.rect.y -= self.speed

        # Check if the player has exceeded the screen borders
        if self.rect.right > WIDTH:  # If player exceeds right border
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top= 0

        # If the player's position has changed, update its center position
        if self.rect.x != current_x or self.rect.y != current_y:
            self.rect.center = self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2


class Door(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = pygame.image.load('gamejab/materials/professor2.png')
        self.image = pygame.transform.scale(self.image_orig, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, HEIGHT // 2)

        