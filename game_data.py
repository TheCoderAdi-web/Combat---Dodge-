import pygame

class Player():
    def __init__(self, size, pos):
        self.image: pygame.surface.Surface = pygame.surface.Surface(size)
        self.rect = self.image.get_rect()
        self.x: int = pos[0]
        self.y: int = pos[1]
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        dx: int
        dy: int
        dx, dy = 0, 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]: dx += 1
        if keys[pygame.K_LEFT]: dx -= 1
        if keys[pygame.K_UP]: dy -= 1
        if keys[pygame.K_DOWN]: dy += 1

        self.rect.x = dx
        self.rect.y = dy

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))