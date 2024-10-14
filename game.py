import pygame
import sys

class ZombieShooter:

    def __init__(self, screen, window_width, window_height):
        self.screen = screen
        self.window_width = window_width
        self.window_height = window_height

    def game_over(self):
        game_over_font = pygame.font.SysFont(None, 100)  # Font size 100 for a big message

        # Render the "You Died" message
        game_over_surface = game_over_font.render('You Died', True, (255, 0, 0))  # Red text
        game_over_rect = game_over_surface.get_rect(center=(self.window_width // 2, self.window_height // 2))

        # Blit the message to the screen
        self.screen.blit(game_over_surface, game_over_rect)

        # Update the display to show the message
        pygame.display.flip()

        # Pause for 2 seconds (2000 milliseconds) before quitting
        pygame.time.wait(2000)

        # Quit the game
        pygame.quit()
        sys.exit()