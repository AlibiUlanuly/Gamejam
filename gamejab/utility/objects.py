import pygame
from pygame.locals import *
from utility import *
from utility.entities import *

class Object(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, scale=None):
        super().__init__()
        self.image_orig = pygame.image.load(image_path)
        if scale:
            self.image_orig = pygame.transform.scale(self.image_orig, scale)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update_hitbox(self, x, y):
        self.hitbox.topleft = (x, y)


class Door(Object):
    def __init__(self, x, y):
        super().__init__('gamejab/materials/objects/door1.png', x, y)

class Table(Object):
    def __init__(self, x, y):
        super().__init__('gamejab/materials/objects/table.png', x, y, (200, 200))

class Desk(Object):
    def __init__(self, x, y):
        super().__init__('gamejab/materials/objects/desk.png', x, y, (300, 300))

class Adapter(Object):
    def __init__(self, x, y):
        super().__init__('gamejab/materials/objects/adapter1.png', x, y, (70, 70))