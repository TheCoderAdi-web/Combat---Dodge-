import pygame
import sys
from random import randrange, choice
from typing import Optional

"""Define all Global Variables."""
RESOLUTION: tuple = (1000, 800)
FPS: int = 60

"""
A Dictionary for the properties of Each Enemy Type.
Format: Name: (Speed, Health, Image Path for Loading)
"""
ENEMY_TYPE_PROPERTIES = {
    "Normal": (4, 2, "images/enemies/normal.png"),
    "Speedster": (6, 1, "images/enemies/speedster.png"),
    "Giant": (2, 4, "images/enemies/giant.png")
}

class Game():
    """Object to contain all of the game elements. Like the main operator class."""
    def __init__(self):
        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("Combat & Dodge")

        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.player: Player = Player((515, 415), self)

        self.enemies: pygame.sprite.Group = pygame.sprite.Group()

        self.enemy_timer_max: int = 200
        self.enemy_timer: int = self.enemy_timer_max

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
            enemy_type_names: list[str] = list(ENEMY_TYPE_PROPERTIES.keys())
            enemy_type: str = choice(enemy_type_names)
            self.enemy_timer = self.enemy_timer_max
            self.enemies.add(Enemy((RESOLUTION[0], randrange(0, RESOLUTION[1])), enemy_type))

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
    def __init__(self, pos: tuple[int, int], game: Game):
        self.image: pygame.surface.Surface = pygame.image.load("images/player.png").convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.x_float: float = float(self.rect.x)
        self.y_float: float = float(self.rect.y)
        self.game = game
        self.attack_rect: Optional[pygame.Rect] = None
        self.attack_rect_size: tuple = (50, 20)
        self.attack_timer_max: int = 15
        self.attack_timer: int = self.attack_timer_max
        self.attacked: bool = False

    def init_attack(self):
        """Initialize the attack_rect object when Attacking"""
        self.attack_rect = pygame.Rect(0, 0, self.attack_rect_size[0], self.attack_rect_size[1])
        self.attack_rect.left = self.rect.right + 2
        self.attack_rect.centery = self.rect.centery
        self.attack_timer = self.attack_timer_max
        self.attacked = True

    def update(self, move_speed: int) -> Optional[str]:
        """Handle movement, attacking, and collisions"""
        dx: float
        dy: float
        dx, dy = 0.0, 0.0

        # Player attacking logic
        if self.attacked:
            self.attack_timer -= 1 

            if self.attack_rect != None:
                for enemy in self.game.enemies:
                    if self.attack_rect.colliderect(enemy.rect):
                        enemy.health -= 1
                        self.attack_rect = None
                        break

            if self.attack_timer <= 0:
                self.attack_rect = None
                self.attacked = False

        keys: tuple[int, ...] = pygame.key.get_pressed()

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
    def __init__(self, pos: tuple[int, int], type: str):
        super().__init__()

        self.type: str = type
        self.move_speed: int = ENEMY_TYPE_PROPERTIES[self.type][0]
        self.health: int = ENEMY_TYPE_PROPERTIES[self.type][1]
        self.image: pygame.surface.Surface = pygame.image.load(ENEMY_TYPE_PROPERTIES[self.type][2]).convert_alpha()
        
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        """
        Updating the enemy's position and killing it once it
        goes off screen.
        """
        # Enemy moves left by 1 pixel each frame
        dx: int = self.move_speed
        self.rect.x -= dx

        # Check for the enemies health
        if self.health <= 0:
            self.kill()

        # Check if the enemy is entirely off the left side of the screen
        if self.rect.right < 0:
            self.kill()