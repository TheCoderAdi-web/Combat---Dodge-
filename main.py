"""Importing and Initializing Packages/Modules."""
import pygame
from game_data import Game
pygame.init()

if __name__ == "__main__":
    """Run the game"""
    game: Game = Game()
    game.run()