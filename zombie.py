import random
import pygame
import math
from util import *

class Zombie:
    def __init__(self, world_width, world_height, zombie_size=50, zombie_speed=1):
        # Spawn the zombie at a random position around the edges of the map
        self.zombie_size = zombie_size
        self.zombie_color = (0, 255, 0)
        self.world_width = world_width
        self.world_height = world_height
        self.zombie_speed = zombie_speed

        self.x, self.y = self.spawn()

        self.rect = pygame.Rect(self.x, self.y, self.zombie_size, self.zombie_size)

    def spawn(self):
        """Spawns a zombie at a random location around the edges of the world."""
        spawn_positions = [
            (random.randint(0, self.world_width - self.zombie_size), 0),  # Top edge
            (random.randint(0, self.world_width - self.zombie_size), self.world_height - self.zombie_size),  # Bottom edge
            (0, random.randint(0, self.world_height - self.zombie_size)),  # Left edge
            (self.world_width - self.zombie_size, random.randint(0, self.world_height - self.zombie_size))  # Right edge
        ]
        return random.choice(spawn_positions)

    def move_toward_player(self, player_x, player_y, walls):
        """Moves the zombie toward the player's position."""
        dx, dy = player_x - self.x, player_y - self.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx, dy = dx / distance, dy / distance  # Normalize
        
        new_x = self.x + dx * self.zombie_speed
        new_rect = pygame.Rect(new_x, self.y, self.zombie_size, self.zombie_size)
        if not check_wall_collision(new_rect, walls):
            self.x = new_x

        new_y = self.y + dy * self.zombie_speed
        new_rect = pygame.Rect(self.x, new_y, self.zombie_size, self.zombie_size)
        if not check_wall_collision(new_rect, walls):
            self.y = new_y
        
        self.rect.topleft = (self.x, self.y)

    def check_bullet_collision(self, bullets):
        """Checks for collision between zombies and bullets."""
        for bullet in bullets:
            if self.rect.colliderect(bullet.rect):
                bullets.remove(bullet)
                return True  # Return True if collision happened, so the zombie can be removed
        return False

    def draw(self, screen, camera_x, camera_y):
        """Draws the zombie as a green rectangle."""
        # pygame.draw.rect(screen, self.zombie_color, self.rect)
        pygame.draw.rect(screen, self.zombie_color, (self.rect.x - camera_x, self.rect.y - camera_y, self.zombie_size, self.zombie_size))