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
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

game = ZombieShooter(window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT, screen=screen)

pygame.display.set_caption('Zombie Shooter')


font = pygame.font.SysFont(None, 36)  # Font size 36

# Setup clock for frame rate
clock = pygame.time.Clock() 

# Define colors (for testing purposes)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (1, 50, 32)
LIGHT_BROWN = (181, 101, 29)

player = Player(world_height=WORLD_HEIGHT, world_width=WORLD_WIDTH)

bullets = []
zombies = []

# Camera (viewport) offset
camera_x = 0
camera_y = 0


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
                # bullet = Bullet(player_x + player_size // 2, player_y + player_size // 2, player.direction)
                bullet = Bullet(player.x, player.y, player.direction)
                bullets.append(bullet)
                print("Space pressed. Bullet fired")

    if len(zombies) < 5 and random.randint(1, 100) < 3:  # 3% chance of spawning a zombie per frame
        zombies.append(Zombie(world_height=WORLD_HEIGHT, world_width=WORLD_WIDTH, size=80))  # Instantiate a new zombie

    # Get key presses
    keys = pygame.key.get_pressed()
        
    new_player_x = player.x
    if keys[pygame.K_a]:  # Left
        new_player_x -= player.speed
        player.direction = "left"
    if keys[pygame.K_d]:  # Right
        new_player_x += player.speed
        player.direction = "right"

    new_player_rect = pygame.Rect(new_player_x, player.y, player.size, player.size)

    collision = check_collision(new_player_rect, walls)

    if not collision:
        player.x = new_player_x
    

    new_player_y = player.y
    if keys[pygame.K_w]:  # Up
        new_player_y -= player.speed
        player.direction = "up"
    if keys[pygame.K_s]:  # Down
        new_player_y += player.speed
        player.direction = "down"

    new_player_rect = pygame.Rect(player.x, new_player_y, player.size, player.size)

    collision = check_collision(new_player_rect, walls)

    if not collision:
        player.y = new_player_y

    # Check for collision with walls
    collision = False
    
    # Update camera position (centered on player)
    camera_x = player.x - WINDOW_WIDTH // 2
    camera_y = player.y - WINDOW_HEIGHT // 2

    # Keep camera within world bounds
    camera_x = max(0, min(camera_x, WORLD_WIDTH - WINDOW_WIDTH))
    camera_y = max(0, min(camera_y, WORLD_HEIGHT - WINDOW_HEIGHT))


    # Move zombies toward player and check for collisions with bullets
    zombies_temp = []
    for zombie in zombies:
        if check_collision(zombie.rect, bullets):
            player.score += 1
            bullets.remove(bullet)
        elif check_collision(zombie.rect, [player.rect]):
            player.health -= 1
        else:
            zombies_temp.append(zombie)
    
    zombies = zombies_temp


    for zombie in zombies:
        zombie.move_toward_player(player.x, player.y, walls)

    # Drawing
    screen.fill(LIGHT_BROWN)  # Fill the screen with white (background)

    score_surface = font.render(f'Score: {player.score}', True, (0, 0, 0))  # Render the score with black color
    screen.blit(score_surface, (10, 10))  # Draw the score at the top-left corner (10, 10)
    health_surface = font.render(f'Health: {player.health}', True, (0, 0, 0))  # Render the score with black color
    screen.blit(health_surface, (10, 35))  # Draw the score at the top-left corner (10, 10)


    # Move and draw bullets
    for bullet in bullets:
        bullet.move()
        bullet.draw(screen, camera_x, camera_y)

    # Draw zombies
    # for zombie in zombies:
    #     zombie.draw(screen, camera_x, camera_y)

    # Draw the player (adjusted for the camera position)
    player_image = player.images[player.direction]
    player.rect = player_image.get_rect(center=(player.x, player.y))

    for zombie in zombies:
        zombie_image = zombie.images[zombie.direction]
        zombie.rect = zombie_image.get_rect(center=(zombie.x, zombie.y))
        screen.blit(zombie_image, (zombie.x - camera_x, zombie.y - camera_y))


    screen.blit(player_image, (player.x - camera_x, player.y - camera_y))
    
    # Draw the world boundaries for testing
    pygame.draw.rect(screen, RED, (0 - camera_x, 0 - camera_y, WORLD_WIDTH, WORLD_HEIGHT), 5)

    for wall in walls:
        pygame.draw.rect(screen, DARK_GREEN, (wall.x - camera_x, wall.y - camera_y, wall.width, wall.height))

    # Update the display
    pygame.display.flip()

    if player.health <= 0:
        game.game_over()

    # Cap the frame rate
    clock.tick(FPS)