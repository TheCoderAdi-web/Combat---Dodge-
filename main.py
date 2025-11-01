"""Importing and Initializing Packages/Modules."""
import pygame
from game_data import Game
pygame.init()


"""Run the game"""
if __name__ == "__main__":
    game: Game = Game()
    game.run()