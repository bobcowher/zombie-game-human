import pygame
import sys
import math
from zombie import Zombie
from bullet import Bullet
import random

# Initialize PyGame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800  # Visible game window size
WORLD_WIDTH, WORLD_HEIGHT = 1600, 1200  # The size of the larger game world
FPS = 60

# Setup display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Zombie Shooter')

# Setup clock for frame rate
clock = pygame.time.Clock() 

# Define colors (for testing purposes)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (1, 50, 32)
LIGHT_BROWN = (181, 101, 29)

# Player settings
player_size = 50
player_color = GREEN
player_speed = 5

# Player initial position in the world (center of the larger world)
player_x = WORLD_WIDTH // 2
player_y = WORLD_HEIGHT // 2

player_images = {}

for direction in ('up', 'down', 'left', 'right'):
    image = pygame.image.load(f'images/player_{direction}.png')
    player_images[direction] = pygame.transform.scale(image, (player_size, player_size))

player_direction = "up"

bullets = []
zombies = []

# Camera (viewport) offset
camera_x = 0
camera_y = 0

def collision_check(rect, walls, camera_x, camera_y):
    # Check for horizontal collision
    for wall in walls:
        # if rect.colliderect(wall.x - camera_x + 25, wall.y - camera_y + 25, wall.width, wall.height):
        if(rect.colliderect(wall)):
            return True
    
    return False

# Define walls as a list of rectangles (x, y, width, height)
walls = [
    pygame.Rect(200, 200, 400, 50),  # A horizontal wall
    pygame.Rect(850, 500, 50, 400),  # A vertical wall
    pygame.Rect(1000, 1000, 300, 50), # Another horizontal wall
    # Add more walls as needed
]

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Shooting event: spacebar to fire bullets
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # bullet = Bullet(player_x + player_size // 2, player_y + player_size // 2, player_direction)
                bullet = Bullet(player_x, player_y, player_direction)
                bullets.append(bullet)
                print("Space pressed. Bullet fired")

    if len(zombies) < 5 and random.randint(1, 100) < 3:  # 3% chance of spawning a zombie per frame
        zombies.append(Zombie(world_height=WORLD_HEIGHT, world_width=WORLD_WIDTH))  # Instantiate a new zombie

    # Get key presses
    keys = pygame.key.get_pressed()
    
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    
    new_player_x = player_x
    if keys[pygame.K_a]:  # Left
        new_player_x -= player_speed
        player_direction = "left"
    if keys[pygame.K_d]:  # Right
        new_player_x += player_speed
        player_direction = "right"

    new_player_rect = pygame.Rect(new_player_x, player_y, player_size, player_size)

    collision = collision_check(rect=new_player_rect, walls=walls, camera_x=camera_x, camera_y=camera_y)

    if not collision:
        player_x = new_player_x
    

    new_player_y = player_y
    if keys[pygame.K_w]:  # Up
        new_player_y -= player_speed
        player_direction = "up"
    if keys[pygame.K_s]:  # Down
        new_player_y += player_speed
        player_direction = "down"

    new_player_rect = pygame.Rect(player_x, new_player_y, player_size, player_size)

    collision = collision_check(rect=new_player_rect, walls=walls, camera_x=camera_x, camera_y=camera_y)

    if not collision:
        player_y = new_player_y

    # Check for collision with walls
    collision = False
    
    # Update camera position (centered on player)
    camera_x = player_x - WINDOW_WIDTH // 2
    camera_y = player_y - WINDOW_HEIGHT // 2

    # Keep camera within world bounds
    camera_x = max(0, min(camera_x, WORLD_WIDTH - WINDOW_WIDTH))
    camera_y = max(0, min(camera_y, WORLD_HEIGHT - WINDOW_HEIGHT))


    # Move zombies toward player and check for collisions with bullets
    zombies = [zombie for zombie in zombies if not zombie.check_bullet_collision(bullets)]
    for zombie in zombies:
        zombie.move_toward_player(player_x, player_y, walls)

    # Drawing
    screen.fill(LIGHT_BROWN)  # Fill the screen with white (background)

    # Move and draw bullets
    for bullet in bullets:
        bullet.move()
        bullet.draw(screen, camera_x, camera_y)

    # Draw zombies
    for zombie in zombies:
        zombie.draw(screen, camera_x, camera_y)

    # Draw the player (adjusted for the camera position)
    player_image = player_images[player_direction]
    # player_rect = player_image.get_rect(center=(player_x - camera_x, player_y - camera_y))
    player_rect = player_image.get_rect(center=(player_x, player_y))

    screen.blit(player_image, (player_x - camera_x, player_y - camera_y))
    
    # Draw the world boundaries for testing
    pygame.draw.rect(screen, RED, (0 - camera_x, 0 - camera_y, WORLD_WIDTH, WORLD_HEIGHT), 5)

    for wall in walls:
        pygame.draw.rect(screen, DARK_GREEN, (wall.x - camera_x, wall.y - camera_y, wall.width, wall.height))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)