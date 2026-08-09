import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from boat import Boat
from player import Player
from level import Level
from ui import UI



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.ui = UI(WIDTH, HEIGHT)
        self.selected_cat = None
        self.player = Player()
        self.level = Level()

        self.water_tiles = [
            pygame.transform.scale(
                pygame.image.load("assets/waterbig1.PNG").convert(),
                (WIDTH, HEIGHT)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/waterbig2.PNG").convert(),
                (WIDTH, HEIGHT)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/waterbig3.PNG").convert(),
                (WIDTH, HEIGHT)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/waterbig4.PNG").convert(),
                (WIDTH, HEIGHT)
            )
        ]

        self.current_water = 0
        self.water_timer = 0

    def draw_water(self):
        self.screen.blit(self.water_tiles[self.current_water], (0, 0))
    def run(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_e:

                        cat = self.level.get_nearby_cat(self.player)

                        if cat is not None:
                            self.selected_cat = cat

                    if event.key == pygame.K_ESCAPE:
                        self.selected_cat = None

            self.water_timer += self.clock.get_time()
            if self.water_timer > 800:
                self.water_timer = 0
                self.current_water = (self.current_water + 1) % 2

            keys = pygame.key.get_pressed()
            old_x = self.player.x
            old_y = self.player.y
            self.player.update(keys)
            self.draw_water()
            self.level.check_boundaries(self.player)
            if self.level.check_collision(self.player.boat):
                self.player.x = old_x
                self.player.y = old_y
                self.player.rect.x = int(self.player.x)
                self.player.rect.y = int(self.player.y)
            self.draw_water()


            self.level.draw(self.screen)
            self.player.draw(self.screen)
            if self.selected_cat is not None:
                self.ui.draw_cat_info(
                    self.screen,
                    self.selected_cat
                )
            pygame.display.flip()
            self.clock.tick(FPS)



        pygame.quit()

