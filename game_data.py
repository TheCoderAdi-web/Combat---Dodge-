import pygame

class Player():
    def __init__(self, size, pos, color):
        self.image: pygame.surface.Surface = pygame.surface.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, move_speed):
        dx: int
        dy: int
        dx, dy = 0, 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]: dx += move_speed
        if keys[pygame.K_LEFT]: dx -= move_speed
        if keys[pygame.K_UP]: dy -= move_speed
        if keys[pygame.K_DOWN]: dy += move_speed

        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)

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
        dx: int = -1 
        self.rect.x += dx

        # Check if the enemy is entirely off the left side of the screen
        if self.rect.right < 0:
            self.kill()