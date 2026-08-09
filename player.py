import pygame
from settings import WIDTH, HEIGHT
from boat import Boat


class Player:
    def __init__(self):
        self.image = pygame.image.load("assets/nyancat.png")
        bounding = self.image.get_bounding_rect()
        self.image = self.image.subsurface(bounding).copy()

        self.image = pygame.transform.scale(self.image, (55, 40))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 130))
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.vx = 0
        self.vy = 0
        self.acceleration = 0.5
        self.max_speed = 3
        self.friction = 0.8

        self.boat = Boat(WIDTH // 2, HEIGHT - 130)

    def draw(self, screen):
        self.boat.draw(screen)
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
        # Begrenzung von max_speed
        self.vx = max(-self.boat.speed, min(self.vx, self.boat.speed))
        self.vy = max(-self.boat.speed, min(self.vy, self.boat.speed))
        # Reibungskraft
        self.vx *= self.friction
        self.vy *= self.friction
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.boat.x = self.x
        self.boat.y = self.y + 50
        self.boat.rect.center = (int(self.boat.x), int(self.boat.y))

        print(keys[pygame.K_UP], self.vy)
