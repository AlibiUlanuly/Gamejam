import pygame
from utility import *
from utility.dialogue import *

background1 = pygame.image.load('gamejab/materials/images/background1.png')
background_image = pygame.transform.scale(background1, (WIDTH, HEIGHT))
background2 = pygame.image.load('gamejab/materials/images/background1.png')

class NPC(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        original_image = pygame.image.load('gamejab/materials/professor/Professor3.png')
        scaled_width = original_image.get_width() // 4
        scaled_height = original_image.get_height() // 4
        self.image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        self.rect.center = (600, 300)

        self.screen = screen
        self.dialogue_lines = dialogue_script[:]  # Copy of the dialogue script
        self.dialogue_box = DialogueBox(self.screen, self.dialogue_lines)
        self.space_pressed = False  # Flag to indicate if spacebar is pressed

    def interact(self):
        self.space_pressed = True

    def update(self, player, screen):
        if pygame.sprite.collide_rect(self, player):
            self.interact()

        if self.space_pressed:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.dialogue_box.current_line_index += 1
                if self.dialogue_box.current_line_index >= len(self.dialogue_lines):
                    self.dialogue_box.current_line_index = 0
                self.space_pressed = False

        if self.space_pressed:
            self.dialogue_box.update()  # Only update the dialogue box when space is pressed




class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__() 
        self.walkFront = [pygame.image.load('gamejab/materials/player/walkfront1.png'), pygame.image.load('gamejab/materials/player/player-back.png'), pygame.image.load('gamejab/materials/player/walkfront2.png'), pygame.image.load('gamejab/materials/player/player-back.png')]
        self.walkDown = [pygame.image.load('gamejab/materials/player/walkdown1.png'), pygame.image.load('gamejab/materials/player/player-standing.png'), pygame.image.load('gamejab/materials/player/walkdown2.png'), pygame.image.load('gamejab/materials/player/player-standing.png')]
        self.walkRight = [pygame.image.load('gamejab/materials/player/walkright1.png'), pygame.image.load('gamejab/materials/player/player-right.png'), pygame.image.load('gamejab/materials/player/walkright2.png'), pygame.image.load('gamejab/materials/player/player-right.png')]
        self.walkLeft = [pygame.image.load('gamejab/materials/player/walkleft1.png'), pygame.image.load('gamejab/materials/player/player-left.png'), pygame.image.load('gamejab/materials/player/walkleft2.png'), pygame.image.load('gamejab/materials/player/player-left.png')]
        self.walkcount = 0
        self.image = pygame.image.load('gamejab/materials/player/player-standing.png')  # Load your player image here
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
        self.image = pygame.image.load('gamejab/materials/objects/door1.png')
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, HEIGHT // 2)


class DialogueBox:
    def __init__(self, screen, dialogue_lines):
        self.screen = screen
        self.dialogue_lines = dialogue_lines
        self.font = pygame.font.SysFont(None, 24)
        self.dialogue_box = pygame.Surface((WIDTH - 40, 150))  # Adjusted width to fit the screen
        self.dialogue_box.fill((139, 69, 19))  # Brown color
        self.dialogue_rect = self.dialogue_box.get_rect(center=(WIDTH // 2, HEIGHT - 75))  # Centered at the bottom of the screen
        self.current_line_index = 0  # Index of the current dialogue line

    def update(self):
        if self.current_line_index < len(self.dialogue_lines):
            # Render the dialogue box
            self.screen.blit(self.dialogue_box, self.dialogue_rect)
            # Render the current dialogue line
            current_line = self.dialogue_lines[self.current_line_index]
            rendered_lines = self.render_text(current_line)
            y_offset = 10
            for line in rendered_lines:
                text_surface = self.font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(WIDTH // 2, self.dialogue_rect.y + y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += self.font.get_height() + 5  # Add space between lines

    def render_text(self, text):
        max_width = WIDTH - 80  # Maximum width for text in dialogue box
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if self.font.size(current_line + word)[0] < max_width:
                current_line += (word + " ")
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        return lines

