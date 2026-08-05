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
        self.water_frames = [
            pygame.transform.scale(
                pygame.image.load("assets/waterbig1.PNG").convert(),
                (WIDTH, HEIGHT)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/waterbig2.PNG").convert(),
                (WIDTH, HEIGHT)
            )
        ]

        self.current_water = 0
        self.water_timer = 0

    def draw_water(self):
        self.screen.blit(self.water_frames[self.current_water], (0, 0))
    def run(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.water_timer += self.clock.get_time()
            if self.water_timer > 600:
                self.water_timer = 0
                self.current_water = (self.current_water + 1) % 2
            self.draw_water()
            keys = pygame.key.get_pressed()
            self.player.update(keys)

            self.player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

