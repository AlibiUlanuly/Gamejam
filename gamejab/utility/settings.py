import pygame
import sys
from pygame.locals import *

pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

FPS = 60

VELOCITY = 4

WIDTH, HEIGHT = 800, 800

ROWS = COLS = 50

PIXEL_SIZE = WIDTH//COLS
