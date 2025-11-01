import pygame
import sys
from random import randrange
from typing import Optional

"""Define all Global Variables."""
RESOLUTION: tuple = (1000, 800)
FPS = 60

class Game():
    """Object to contain all of the game elements. Like the main operator class."""
    def __init__(self):
        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("Combat & Dodge")

        self.clock = pygame.time.Clock()

        self.player = Player((64, 64), (515, 415), "red", self)

        self.enemies = pygame.sprite.Group()

        self.enemy_timer_max = 200
        self.enemy_timer = self.enemy_timer_max

    def draw(self):
        self.screen.fill("black")
        self.enemies.draw(self.screen)
        self.player.draw()
        pygame.display.flip()

    def update(self):
        if self.player.update(4) == "game_over":
            pygame.quit()
            sys.exit()
            
        self.enemies.update()

    def spawn_enemies(self):
        if self.enemy_timer > 0:
            self.enemy_timer -= 1
        else:
            self.enemy_timer = self.enemy_timer_max
            self.enemies.add(Enemy((RESOLUTION[0], randrange(0, RESOLUTION[1]))))

    def run(self):
        """Simply run the game, and include all drawing and update functions."""
        running: bool = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

            self.draw()
            self.update()
            self.spawn_enemies()

            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

class Player():
    """Player class"""
    def __init__(self, size, pos, color, game):
        self.image: pygame.surface.Surface = pygame.surface.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.x_float: float = float(self.rect.x)
        self.y_float: float = float(self.rect.y)
        self.game = game
        self.attack_rect: Optional[pygame.Rect] = None
        self.attack_rect_size: tuple = (50, 30)
        self.attack_timer_max: int = 30
        self.attack_timer: int = self.attack_timer_max
        self.attacked: bool = False

    def init_attack(self):
        """Initialize the attack_rect object when Attacking"""
        self.attack_rect = pygame.Rect(0, 0, self.attack_rect_size[0], self.attack_rect_size[1])
        self.attack_rect.left = self.rect.right + 2
        self.attack_rect.centery = self.rect.centery
        self.attack_timer: int = self.attack_timer_max
        self.attacked = True

    def update(self, move_speed) -> Optional[str]:
        """Handle movement, attacking, and collisions"""
        dx: float
        dy: float
        dx, dy = 0.0, 0.0

        # Player attacking logic
        if self.attacked:
            self.attack_timer -= 1 
            
            for enemy in self.game.enemies:
                if self.attack_rect != None and self.attack_rect.colliderect(enemy.rect):
                    enemy.kill()

            if self.attack_timer <= 0:
                self.attack_rect = None
                self.attacked = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not self.attacked:
            self.init_attack()

        # Basic Player Movement
        if keys[pygame.K_RIGHT]: dx += move_speed
        if keys[pygame.K_LEFT]: dx -= move_speed
        if keys[pygame.K_UP]: dy -= move_speed
        if keys[pygame.K_DOWN]: dy += move_speed
        
        # Updating the player's position based on dx, dy variables
        self.x_float += dx
        self.y_float += dy

        self.rect.x = int(self.x_float)
        self.rect.y = int(self.y_float)

        # Checking for direct collision with enemies, and returning
        # a game_over message if the collision is succesful.
        for enemy in self.game.enemies:
            if self.rect.colliderect(enemy.rect):
                return "game_over"

    def draw(self):
        """Drawing the player, and optionally drawing the attack_rect"""
        self.game.screen.blit(self.image, self.rect)

        # Draw the Attack Rect (For Debugging)
        if self.attack_rect != None: pygame.draw.rect(surface=self.game.screen, color="green", rect=self.attack_rect)

class Enemy(pygame.sprite.Sprite):
    """
    Enemy Class.
    No need for drawing as the Enemies are drawn
    using a Pygame Sprite Group called enemies in
    the Game class, defined in main.py.
    """
    def __init__(self, pos):
        super().__init__() 
        
        self.image: pygame.surface.Surface = pygame.surface.Surface((64, 64))
        self.image.fill("blue")
        
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        """
        Updating the enemy's position and killing it once it
        goes off screen.
        """
        # Enemy moves left by 1 pixel each frame
        dx: int = -4 
        self.rect.x += dx

        # Check if the enemy is entirely off the left side of the screen
        if self.rect.right < 0:
            self.kill()