import pygame
from utility import *
from utility.dialogue import *

background1 = pygame.image.load('gamejab/materials/images/background1.png')
background_image = pygame.transform.scale(background1, (WIDTH, HEIGHT))
background2 = pygame.image.load('gamejab/materials/images/background2.png')
background_image2 = pygame.transform.scale(background2, (WIDTH, HEIGHT))
background3 = pygame.image.load('gamejab/materials/images/background3.png')
background_image3 = pygame.transform.scale(background3, (WIDTH, HEIGHT))

class NPC(pygame.sprite.Sprite):
    def __init__(self, screen, event1, event2, event3, questions):
        super().__init__()
        original_image = pygame.image.load('gamejab/materials/professor/Professor3.png')
        scaled_width = original_image.get_width() // 4
        scaled_height = original_image.get_height() // 4
        self.image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()

        self.rect.center = (600, 300)
        
        self.screen = screen
        
        self.event1 = event1
        self.event2 = event2
        self.event3 = event3
        self.questions = questions
        self.dialogue_lines = dialogue_script[:]
        
        # Copy of the dialogue script
    
        self.dialogue_box = DialogueBox(self.screen, self.dialogue_lines)
        self.dialogue_active = False
        self.space_was_pressed = False
        self.current_line_index = 0  # Index of the current dialogue line
        
        self.portrait_image = pygame.image.load('gamejab/materials/professor/professor-half.png')  # Adjust the path as necessary
        self.portrait_image = pygame.transform.scale(self.portrait_image, (200, 200))  # Adjust size as needed

    
    def update(self, player, screen):
   
        keys = pygame.key.get_pressed()
        if pygame.sprite.collide_rect(self, player):
            if keys[pygame.K_SPACE] and not self.dialogue_active and not self.space_was_pressed:
                self.dialogue_active = True
                self.space_was_pressed = True
                if self.event2.completed:
                    self.dialogue_lines = dialogue_script2[:]
                    self.current_line_index = 0
                else:
                    self.dialogue_lines = dialogue_script[:]
                self.dialogue_box = DialogueBox(self.screen, self.dialogue_lines)
            elif not keys[pygame.K_SPACE]:
                self.space_was_pressed = False

        if self.dialogue_active:
            # Render professor image on the left side of the dialogue box

            self.dialogue_box.update()
            self.dialogue_box.display_portrait(self.portrait_image, 0, 650)

            if keys[pygame.K_SPACE] and not self.space_was_pressed:
                self.current_line_index += 1
                if self.current_line_index >= len(self.dialogue_lines):
                    self.current_line_index = 0
                    self.dialogue_active = False
                    if self.event1.completed == False:
                        self.event1.completed = True
                    if self.event2.completed == True and self.event3.completed == False:  # Check if event2 is completed and event3 is not yet completed
                        self.event3.completed = True 

            # Reset dialogue box with updated index
                self.dialogue_box.current_line_index = self.current_line_index
                self.space_was_pressed = True
            elif not keys[pygame.K_SPACE]:
                self.space_was_pressed = False
               
    



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


class DialogueBox:
    def __init__(self, screen, dialogue_lines):
        self.screen = screen
        self.dialogue_lines = dialogue_lines
        self.font = pygame.font.SysFont(None, 24)
        self.dialogue_box_width = WIDTH - 40
        self.dialogue_box_height = 150
        self.dialogue_box = pygame.Surface((self.dialogue_box_width, self.dialogue_box_height))  
        self.dialogue_box.fill((139, 69, 19))  # Brown color
        self.dialogue_rect = self.dialogue_box.get_rect(center=(WIDTH // 2, HEIGHT - 75)) 
        self.current_line_index = 0  
        self.overlay_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay_surface.fill((0, 0, 0, 128))
        self.border_color = (255, 255, 255)
        self.border_thickness = 2

    def update(self):
        self.screen.blit(self.overlay_surface, (0, 0))

        if self.current_line_index < len(self.dialogue_lines):
            # Render the dialogue box border
            pygame.draw.rect(self.screen, self.border_color, self.dialogue_rect, self.border_thickness)
            # Render the dialogue box
            self.screen.blit(self.dialogue_box, self.dialogue_rect)

            # Render the current dialogue line
            current_line = self.dialogue_lines[self.current_line_index]
            rendered_lines = self.render_text(current_line)
            total_text_height = sum(self.font.size(line)[1] + 5 for line in rendered_lines)
            start_y = self.dialogue_rect.centery - total_text_height // 2

            y_offset = start_y
            for line in rendered_lines:
                text_surface = self.font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.dialogue_rect.centerx, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += self.font.get_height() + 5

    def render_text(self, text):
        max_width = self.dialogue_box_width - 340  # Maximum width for text in dialogue box
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            # Check if adding the word would exceed the maximum width
            if self.font.size(current_line + word)[0] < max_width:
                current_line += (word + " ")
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        return lines
    
    def display_portrait(self, image, x, y):
        self.screen.blit(image, (x, y))




