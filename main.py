"""Importing and Initializing Packages."""
import pygame
import sys
pygame.init()

"""Define all Global Variables."""
RESOLUTION: tuple = (1000, 800)

class Game():
    """Object to contain all of the game elements. Like the main operator class."""
    def __init__(self, resolution):
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("Combat & Dodge")

    def run():
        """Simply run the game, and include all drawing and update functions."""
        running: bool = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

        pygame.quit()
        sys.quit()


"""Run the game"""
if __name__ == "__main__":
    game: Game = Game(RESOLUTION)
    game.run()