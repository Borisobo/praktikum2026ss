import pygame

class Player:
    def __init__(self):
        self.image = pygame.image.load("assets/boat.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, (256, 200))

        self.rect = self.image.get_rect(center=(640,340))
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.vx = 0
        self.vy = 0
        self.acceleration = 0.15
        self.max_speed = 3
        self.friction = 0.92


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.vx -= self.acceleration
        if keys[pygame.K_RIGHT]:
            self.vx += self.acceleration
        if keys[pygame.K_UP]:
            self.vy += self.acceleration
        if keys[pygame.K_DOWN]:
            self.vy -= self.acceleration
