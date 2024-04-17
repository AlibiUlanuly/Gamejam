import pygame
from utility import *

"""
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
char = pygame.image.load('standing.png')
"""
background1 = pygame.image.load('lab8/images/AnimatedStreet.png')
background_image = pygame.transform.scale(background1, (WIDTH, HEIGHT))
background2 = pygame.image.load('lab8/images/AnimatedStreet.png')

class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original_image = pygame.image.load('gamejab/materials/Professor1.png')
        # Define the desired width and height for the scaled image
        scaled_width = original_image.get_width() // 2  # You can adjust this value to your preference
        scaled_height = original_image.get_height() // 2  # You can adjust this value to your preference
        # Scale the original image to the desired size
        self.image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)



class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__() 
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
            self.image = pygame.image.load('gamejab/materials/player-left.png')
            self.rect.x -= self.speed
        if pressed_keys[K_RIGHT]:
            self.image = pygame.image.load('gamejab/materials/player-right.png')
            self.rect.x += self.speed
        if pressed_keys[K_DOWN]:
            self.image = pygame.image.load('gamejab/materials/player-standing.png')
            self.rect.y += self.speed
        if pressed_keys[K_UP]:
            self.image = pygame.image.load('gamejab/materials/player-back.png')
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
        self.image = pygame.image.load('lab8/images/Player.png')
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, HEIGHT // 2)

        