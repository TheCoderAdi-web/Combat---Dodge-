"""Importing and Initializing Packages/Modules."""
import pygame
import sys
from random import randrange
from game_data import Player, Enemy
pygame.init()

"""Define all Global Variables."""
RESOLUTION: tuple = (1000, 800)
FPS = 60

class Game():
    """Object to contain all of the game elements. Like the main operator class."""
    def __init__(self):
        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("Combat & Dodge")

        self.clock = pygame.time.Clock()
        
        self.clock.tick(FPS)

        self.player = Player((30, 30), (515, 415), "red")

        self.enemies = pygame.sprite.Group()

        self.enemy_timer_max = 500
        self.enemy_timer = self.enemy_timer_max

    def run(self):
        """Simply run the game, and include all drawing and update functions."""
        running: bool = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

            self.screen.fill("black")
            
            self.player.update(0.5)
            self.player.draw(self.screen)

            self.enemies.update()
            self.enemies.draw(self.screen)

            if self.enemy_timer > 0:
                self.enemy_timer -= 1
            else:
                self.enemy_timer = self.enemy_timer_max
                self.enemies.add(Enemy((RESOLUTION[0], randrange(0, RESOLUTION[1]))))

            pygame.display.flip()

        pygame.quit()
        sys.exit()


"""Run the game"""
if __name__ == "__main__":
    game: Game = Game()
    game.run()