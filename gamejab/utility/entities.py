import pygame
from utility import *
from utility.dialogue import *

background1 = pygame.image.load('gamejab/materials/images/background1.png')
background_image = pygame.transform.scale(background1, (WIDTH, HEIGHT))
background2 = pygame.image.load('gamejab/materials/images/background2-5.png')
original_width, original_height = background2.get_size()
desired_width, desired_height = WIDTH, HEIGHT

# Calculate the aspect ratio of the original image
aspect_ratio = original_width / original_height

# Calculate the width based on the desired height to maintain the aspect ratio
scaled_width = int(desired_height * aspect_ratio) - 240

# Scale the original image to fit the new width and height
scaled_background = pygame.transform.scale(background2, (scaled_width, desired_height))

# Create a blank surface with the desired dimensions
resized_background = pygame.Surface((desired_width, desired_height))

# Center the scaled image horizontally on the blank surface
x_offset = (desired_width - scaled_width) // 2
resized_background.blit(scaled_background, (x_offset, 0))

# Now you have a resized background image with the desired dimensions and aspect ratio
background_image2 = resized_background



background3 = pygame.image.load('gamejab/materials/images/background3.png')
background_image3 = pygame.transform.scale(background3, (WIDTH, HEIGHT))

class NPC(pygame.sprite.Sprite):
    def __init__(self, screen, event1, event2, event3, questions, event5):
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
        self.event5 = event5
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
                    if self.event5.completed:
                        self.dialogue_lines = dialogue_script3[:]
                        self.current_line_index = 0
                    else:
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
               


class NPC2(pygame.sprite.Sprite):
    def __init__(self, screen, event6):
        super().__init__()
        original_image = pygame.image.load('gamejab/materials/professor/judoprof.png')
        scaled_width = original_image.get_width() // 2
        scaled_height = original_image.get_height() // 2
        self.image = pygame.transform.scale(original_image, (scaled_width + 25,scaled_height + 25))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 400)
        self.screen = screen
        self.portrait_image2 = pygame.image.load('gamejab/materials/professor/judoprof-half.pmg.png')
        self.portrait_image2 = pygame.transform.scale(self.portrait_image2, (200, 200))
        self.event6 = event6

        self.dialogue_lines = dialogue_script4[:]
        self.dialogue_box = DialogueBox(self.screen, self.dialogue_lines)
        self.dialogue_active = False
        self.space_was_pressed = False
        self.current_line_index = 0 

    def update(self, player, screen):

        keys = pygame.key.get_pressed()
        if pygame.sprite.collide_rect(self, player):
            if keys[pygame.K_SPACE] and not self.dialogue_active and not self.space_was_pressed:
                self.dialogue_active = True
                self.space_was_pressed = True

                self.dialogue_box = DialogueBox(self.screen, self.dialogue_lines)
            elif not keys[pygame.K_SPACE]:
                self.space_was_pressed = False

        if self.dialogue_active:
            # Render professor image on the left side of the dialogue box

            self.dialogue_box.update()
            self.dialogue_box.display_portrait(self.portrait_image2, 0, 650)

            if keys[pygame.K_SPACE] and not self.space_was_pressed:
                self.current_line_index += 1
                if self.current_line_index >= len(self.dialogue_lines):
                    self.current_line_index = 0
                    self.dialogue_active = False
                    self.event6.completed = True

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
        self.font = pygame.font.Font('gamejab/materials/fonts/Font2.ttf', 14)
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
            start_y = self.dialogue_rect.centery - total_text_height // 2 + 20

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


class QuizBox:
    def __init__(self, screen, questions, event4):
        self.screen = screen
        self.questions = questions
        self.event4 = event4
        self.font = pygame.font.SysFont(None, 24)
        self.quiz_box_width = WIDTH - 40
        self.quiz_box_height = 200
        self.quiz_box = pygame.Surface((self.quiz_box_width, self.quiz_box_height))
        self.quiz_box.fill((139, 69, 19))  # Black color
        self.quiz_rect = self.quiz_box.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.current_question_index = 0
        self.overlay_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay_surface.fill((0, 0, 0, 128))
        self.border_color = (255, 255, 255)
        self.border_thickness = 2
        self.selected_option = None
        self.option_index = 0  # Index of currently selected option
        self.correct_answers = 0

    def update(self):
        self.screen.blit(self.overlay_surface, (0, 0))

        # Render the quiz box border
        pygame.draw.rect(self.screen, self.border_color, self.quiz_rect, self.border_thickness)

        # Render the quiz box
        self.screen.blit(self.quiz_box, self.quiz_rect)

        # Render the current question and options
        question_surface = self.font.render(self.questions[self.current_question_index]["question"], True, (255, 255, 255))
        question_rect = question_surface.get_rect(center=(WIDTH // 2, self.quiz_rect.y + 30))
        self.screen.blit(question_surface, question_rect)

        option_y = self.quiz_rect.y + 70
        for i, option in enumerate(self.questions[self.current_question_index]["options"]):
            option_surface = self.font.render(option, True, (255, 255, 255))
            option_rect = option_surface.get_rect(center=(WIDTH // 2, option_y))
            self.screen.blit(option_surface, option_rect)
            if i == self.option_index:
                pygame.draw.rect(self.screen, (255, 0, 0), option_rect, 2)  # Highlight selected option
            option_y += 30

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.option_index = (self.option_index - 1) % len(self.questions[self.current_question_index]["options"])
            elif event.key == pygame.K_DOWN:
                self.option_index = (self.option_index + 1) % len(self.questions[self.current_question_index]["options"])
            elif event.key == pygame.K_RETURN:
                self.selected_option = self.questions[self.current_question_index]["options"][self.option_index]
            # Move to the next question if not the last question
                if self.selected_option == self.questions[self.current_question_index]["correct_answer"]:
                    self.correct_answers += 1
                    print('good job')
                else:
                    print('incorrect')

                if self.current_question_index < len(self.questions) - 1:
                    self.current_question_index += 1
                else:
                    self.event4.completed = True
    

    def get_selected_option(self):
        return self.selected_option

