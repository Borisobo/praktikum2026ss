import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.player = Player()

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill((70, 170, 255))
            keys = pygame.key.get_pressed()
            self.player.update(keys)

            self.player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

