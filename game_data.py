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
ENEMY_TYPE_PROPERTIES: dict[str, tuple[float, int, str]] = {
    "Normal": (0.75, 2, "images/enemies/normal.png"),
    "Speedster": (1.0, 1, "images/enemies/speedster.png"),
    "Giant": (0.25, 4, "images/enemies/giant.png")
}

class Game():
    """
    Object to contain all of the game elements. Like the manager of the game.
    """
    def __init__(self) -> None:
        self.screen: pygame.surface.Surface = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("Combat & Dodge")

        self.game_surface: pygame.surface.Surface = pygame.surface.Surface(RESOLUTION)

        self.shake_timer: int = 0
        self.shake_intensity: int = 0

        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.player: Player = Player((515, 415), self)

        self.enemies: pygame.sprite.Group = pygame.sprite.Group()

        self.enemy_timer_max: int = 200
        self.enemy_timer: int = self.enemy_timer_max
        
        self.game_state: str = "running"

    def trigger_shake(self, duration: int, intensity: int) -> None:
        """Starts the screen shake."""
        self.shake_timer = duration
        self.shake_intensity = intensity

    def draw(self) -> None:
        self.game_surface.fill("black")

        self.enemies.draw(self.game_surface)
        self.player.draw()

        draw_offset: tuple[int, int] = (0, 0)

        if self.shake_timer > 0:
            self.shake_timer -= 1

            offset_x: int = randrange(-self.shake_intensity, self.shake_intensity + 1)
            offset_y: int = randrange(-self.shake_intensity, self.shake_intensity + 1)
            draw_offset = (offset_x, offset_y)

        self.screen.fill("black")

        self.screen.blit(self.game_surface, draw_offset)

        pygame.display.flip()

    def update(self) -> None:
        """End the game the moment the player loses"""
        if self.game_state == "running":
            if self.player.update(4) == "game_over":
                self.game_state = "game_over"
            
            self.enemies.update()
            self.spawn_enemies()
            
        elif self.game_state == "game_over":
            self.enemies.update()
            self.player.death_animation()
            
            if self.player.death_timer <= 0:
                pygame.quit()
                sys.exit()

    def spawn_enemies(self) -> None:
        """
        Spawn enemies by randomly picking a type of enemy, and then spawning the enemy.
        """
        if self.enemy_timer > 0:
            self.enemy_timer -= 1
        else:
            enemy_type_names: list[str] = list(ENEMY_TYPE_PROPERTIES.keys())
            enemy_type: str = choice(enemy_type_names)
            self.enemy_timer = self.enemy_timer_max
            self.enemies.add(Enemy((RESOLUTION[0], randrange(0, RESOLUTION[1])), enemy_type))

    def run(self) -> None:
        """Simply run the game, and include all drawing and update functions."""
        running: bool = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

            self.draw()
            self.update()

            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

class Player():
    """Player class"""
    def __init__(self, pos: tuple[int, int], game: Game) -> None:
        self.master_image: pygame.surface.Surface = pygame.image.load("images/player.png").convert_alpha()
        self.hit_image: pygame.surface.Surface = self.master_image.copy()
        self.hit_image.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
        self.image: pygame.surface.Surface = self.master_image.copy()
        self.attack_image: pygame.surface.Surface = pygame.image.load("images/player_attack.png").convert_alpha()
        
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
        self.dx: float
        self.dy: float
        self.dx, self.dy = 0.0, 0.0
        
        self.is_alive: bool = True
        self.death_timer: int = 0
        self.death_timer_max: int = 25

    def init_attack(self) -> None:
        """Initialize the attack_rect object when Attacking"""
        self.attack_rect = pygame.Rect(0, 0, self.attack_rect_size[0], self.attack_rect_size[1])
        self.attack_rect.left = self.rect.right + 2
        self.attack_rect.centery = self.rect.centery
        self.attack_timer = self.attack_timer_max
        self.attacked = True

    def death_animation(self) -> None:
        """
        Main Death Animation logic:
        1. Turning the Player image white to show damage
        2. Shaking the Screen
        3. When the Death Animation is over, Quit the game
        """
        if self.death_timer > 0:
            self.death_timer -= 0.5
        
        self.game.trigger_shake(2, 8)

    def update(self, move_speed: int) -> Optional[str]:
        """Handle movement, attacking, and collisions"""
        if not self.is_alive:
            self.dx *= 0.65
            self.dy *= 0.65
            self.x_float += self.dx
            self.y_float += self.dy
            self.rect.x = int(self.x_float)
            self.rect.y = int(self.y_float)
            self.attack_rect = None
            return None
        
        if self.attacked:
            self.attack_timer -= 1 

            if self.attack_rect != None:
                for enemy in self.game.enemies:
                    if self.attack_rect.colliderect(enemy.rect):
                        self.game.trigger_shake(25, 4)
                        enemy.current_speed -= enemy.current_speed * 3
                        enemy.hit_timer = enemy.hit_timer_max
                        enemy.health -= 1
                        self.attack_rect = None
                        break

            if self.attack_timer <= 0:
                self.attack_rect = None
                self.attacked = False

        keys: tuple[int, ...] = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]: self.dx += move_speed
        if keys[pygame.K_LEFT]: self.dx -= move_speed
        if keys[pygame.K_UP]: self.dy -= move_speed
        if keys[pygame.K_DOWN]: self.dy += move_speed
        if keys[pygame.K_SPACE] and not self.attacked:
            self.init_attack()
        
        self.dx *= 0.65
        self.dy *= 0.65

        self.x_float += self.dx
        self.y_float += self.dy

        self.rect.x = int(self.x_float)
        self.rect.y = int(self.y_float)

        for enemy in self.game.enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.health -= 9999
                self.death_timer = self.death_timer_max
                self.dx = -100
                self.is_alive = False
                return "game_over"

    def draw(self) -> None:
        """Drawing the player, and optionally drawing the attack_rect"""
        image_to_draw = self.master_image
        if not self.is_alive:
            image_to_draw = self.hit_image
        
        self.game.game_surface.blit(image_to_draw, self.rect)

        if self.attack_rect != None: 
            self.game.game_surface.blit(self.attack_image, self.attack_rect)

class Enemy(pygame.sprite.Sprite):
    """
    Enemy Class.
    No need for drawing as the Enemies are drawn
    using a Pygame Sprite Group called enemies in
    the Game class, defined in main.py.
    """
    def __init__(self, pos: tuple[int, int], type: str) -> None:
        super().__init__()

        self.type: str = type
        self.move_speed: float = ENEMY_TYPE_PROPERTIES[self.type][0]
        self.speed_cap: float = self.move_speed * 8
        self.current_speed: float = 0.0
        self.health: int = ENEMY_TYPE_PROPERTIES[self.type][1]
        
        # --- Master images (never modified) ---
        self.master_image: pygame.surface.Surface = pygame.image.load(ENEMY_TYPE_PROPERTIES[self.type][2]).convert_alpha()
        self.master_hit_image: pygame.surface.Surface = self.master_image.copy()
        self.master_hit_image.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
        
        # --- Current image (overwritten each frame) ---
        self.image: pygame.surface.Surface = self.master_image.copy()
        self.angle: float = 0.0
        
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.hit_timer_max: int = 20
        self.hit_timer: int = 0

    def die(self) -> None:
        """
        Still do the hit frames, and immediately after they end, kill the enemy sprite for a smooth death.
        """
        if self.hit_timer == 0:
            self.kill()
    
    def update(self) -> None:
        """
        Updating the enemy's position and killing it once it
        goes off screen.
        """
        # Enemy's accelaration starts slow, then gains speed till the speed cap
        dx: float = 0.0
        if self.current_speed < self.speed_cap:
            self.current_speed += self.move_speed
        dx = self.current_speed
        self.rect.x -= dx

        # --- Rotation and Image Update Logic ---
        old_center = self.rect.center

        # Rotate the enemy if it is an asteriod
        if self.type == "Normal":
            self.angle = (self.angle - 5) % 360
            rotated_origin = pygame.transform.rotate(self.master_image, self.angle)
            rotated_hit = pygame.transform.rotate(self.master_hit_image, self.angle)
        else:
            # If not "Normal", just use the un-rotated master images
            rotated_origin = self.master_image
            rotated_hit = self.master_hit_image

        # Check for the enemy's health and take damage when it's hit by the player
        if self.hit_timer > 0:
            self.hit_timer -= 1
            self.image = rotated_hit
        else:
            self.image = rotated_origin
        
        # Update the rect with the new image and restore its center
        self.rect = self.image.get_rect(center=old_center)
        # --- End of Rotation Logic ---

        if self.health <= 0:
            self.die()

        # Check if the enemy is entirely off the left side of the screen
        if self.rect.right < 0:
            self.die()