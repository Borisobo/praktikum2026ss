import pygame
from settings import WIDTH, HEIGHT
from boat import Boat

class Player:
    def __init__(self):
        self.image = pygame.image.load("assets/nyancat.png").convert_alpha()
        bounding = self.image.get_bounding_rect()
        self.image = self.image.subsurface(bounding).copy()

        self.image = pygame.transform.scale(self.image, (256, 200))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT - 130))
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.vx = 0
        self.vy = 0
        self.acceleration = 0.5
        self.max_speed = 3
        self.friction = 0.8


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.vx -= self.acceleration
        if keys[pygame.K_RIGHT]:
            self.vx += self.acceleration
        if keys[pygame.K_UP]:
            self.vy -= self.acceleration
        if keys[pygame.K_DOWN]:
            self.vy += self.acceleration
        #Begrenzung von max_speed
        self.vx = max(-self.max_speed, min(self.vx, self.max_speed))
        self.vy = max(-self.max_speed, min(self.vy, self.max_speed))
        # Reibungskraft
        self.vx *= self.friction
        self.vy *= self.friction
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        print(keys[pygame.K_UP], self.vy)


