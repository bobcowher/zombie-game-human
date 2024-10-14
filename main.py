import pygame
import sys
import math
from characters import Zombie, Player
from bullet import Bullet
import random
from util import *
from game import ZombieShooter

# Initialize PyGame
pygame.init()


# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800  # Visible game window size
WORLD_WIDTH, WORLD_HEIGHT = 1600, 1200  # The size of the larger game world
FPS = 60


# Setup display

game = ZombieShooter(window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT, world_height=WORLD_HEIGHT, world_width=WORLD_WIDTH, fps=FPS)

# Define colors (for testing purposes)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


# Camera (viewport) offset
camera_x = 0
camera_y = 0



# Game loop
while True:
    game.step()
