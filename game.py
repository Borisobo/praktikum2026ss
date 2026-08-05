import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from player import Player
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.level = Level()
        self.tile_size = 128
        c = WIDTH // self.tile_size + 1
        r = HEIGHT // self.tile_size + 1
        self.water_tiles = [
            pygame.transform.scale(
                pygame.image.load("assets/water1.PNG").convert(),
                (128, 128)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/water2.PNG").convert(),
                (128, 128)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/water3.PNG").convert(),
                (128, 128)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/water4.PNG").convert(),
                (128, 128)
            )
        ]


        self.current_water = 0
        self.water_timer = 0

    def draw_water(self):
        for row in range(HEIGHT // self.tile_size + 1):
            for col in range(WIDTH // self.tile_size + 1):
                tile_index = (row + col + self.current_water) % 4

                self.screen.blit(
                    self.water_tiles[tile_index],
                    (col * self.tile_size, row * self.tile_size)
                )


    def run(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.water_timer += 1
            if self.water_timer > 15:
                self.water_timer = 0
                self.current_water = (self.current_water + 1) % 4
            self.draw_water()
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            self.level.check_boundaries(self.player)
            
            self.player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

