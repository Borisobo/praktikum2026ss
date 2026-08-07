import pygame


class Island:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load('assets/islands/island1.jpg'), (600, 500))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self,screen):
        screen.blit(self.image, self.rect)

