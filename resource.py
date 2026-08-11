import pygame

class Resources:
    def __init__(self):
        self.fish = 0

        self.fish_image = pygame.image.load("assets/fish.PNG").convert_alpha()
        self.fish_image = pygame.transform.scale(self.fish_image, (40, 40))

        self.font = pygame.font.Font(None, 32)

    def add_fish(self, amount):
        self.fish += amount

    def spend_fish(self, amount):
        if self.fish >= amount:
            self.fish -= amount
            return True
        return False

    def draw(self, screen):
        screen.blit(self.fish_image, (20, 80))

        text = self.font.render(str(self.fish), True, (255, 255, 255))
        screen.blit(text, (70, 85))

