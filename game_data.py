import pygame
from typing import Optional

class Player():
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
        self.attack_rect = pygame.Rect(0, 0, self.attack_rect_size[0], self.attack_rect_size[1])
        self.attack_rect.left = self.rect.right + 2
        self.attack_rect.centery = self.rect.centery
        self.attack_timer: int = self.attack_timer_max
        self.attacked = True

    def update(self, move_speed) -> Optional[str]:
        dx: float
        dy: float
        dx, dy = 0.0, 0.0

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

        if keys[pygame.K_RIGHT]: dx += move_speed
        if keys[pygame.K_LEFT]: dx -= move_speed
        if keys[pygame.K_UP]: dy -= move_speed
        if keys[pygame.K_DOWN]: dy += move_speed
        
        self.x_float += dx
        self.y_float += dy

        self.rect.x = int(self.x_float)
        self.rect.y = int(self.y_float)
        
        for enemy in self.game.enemies:
            if self.rect.colliderect(enemy.rect):
                return "game_over"

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

        # Draw the Attack Rect (For Debugging)
        #if self.attack_rect != None: pygame.draw.rect(surface=self.game.screen, color="green", rect=self.attack_rect, width=3)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__() 
        
        self.image: pygame.surface.Surface = pygame.surface.Surface((60, 60))
        self.image.fill("blue")
        
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        # Enemy moves left by 1 pixel each frame
        dx: int = -4 
        self.rect.x += dx

        # Check if the enemy is entirely off the left side of the screen
        if self.rect.right < 0:
            self.kill()