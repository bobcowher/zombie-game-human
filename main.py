import pygame
import sys

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

# Player settings
player_size = 50
player_color = GREEN
player_speed = 5

# Player initial position in the world (center of the larger world)
player_x = WORLD_WIDTH // 2
player_y = WORLD_HEIGHT // 2

# Camera (viewport) offset
camera_x = 0
camera_y = 0

# Define walls as a list of rectangles (x, y, width, height)
walls = [
    pygame.Rect(200, 200, 400, 50),  # A horizontal wall
    pygame.Rect(800, 500, 50, 400),  # A vertical wall
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


    # Get key presses
    keys = pygame.key.get_pressed()
    
    # Update player position
    if keys[pygame.K_a]:  # Left
        player_x -= player_speed
    if keys[pygame.K_d]:  # Right
        player_x += player_speed
    if keys[pygame.K_w]:  # Up
        player_y -= player_speed
    if keys[pygame.K_s]:  # Down
        player_y += player_speed
    
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    
    # Move the player while checking for collisions
    new_player_x = player_x
    new_player_y = player_y

    if keys[pygame.K_a]:  # Left
        new_player_x -= player_speed
    if keys[pygame.K_d]:  # Right
        new_player_x += player_speed
    if keys[pygame.K_w]:  # Up
        new_player_y -= player_speed
    if keys[pygame.K_s]:  # Down
        new_player_y += player_speed

    # Create a new rect for the future position
    new_player_rect = pygame.Rect(new_player_x, new_player_y, player_size, player_size)

    # Check for collision with walls
    collision = False
    
    for wall in walls:
        if new_player_rect.colliderect(wall):
            collision = True
            break
    
    # Only move if there's no collision
    if not collision:
        player_x = new_player_x
        player_y = new_player_y
    
    # Update camera position (centered on player)
    camera_x = player_x - WINDOW_WIDTH // 2
    camera_y = player_y - WINDOW_HEIGHT // 2

    # Keep camera within world bounds
    camera_x = max(0, min(camera_x, WORLD_WIDTH - WINDOW_WIDTH))
    camera_y = max(0, min(camera_y, WORLD_HEIGHT - WINDOW_HEIGHT))

    # Drawing
    screen.fill(WHITE)  # Fill the screen with white (background)

    # Draw the player (adjusted for the camera position)
    pygame.draw.rect(screen, player_color, (player_x - camera_x, player_y - camera_y, player_size, player_size))
    
    # Draw the world boundaries for testing
    pygame.draw.rect(screen, RED, (0 - camera_x, 0 - camera_y, WORLD_WIDTH, WORLD_HEIGHT), 5)

    for wall in walls:
        pygame.draw.rect(screen, RED, (wall.x - camera_x, wall.y - camera_y, wall.width, wall.height))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)