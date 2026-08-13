import pygame

from settings import WIDTH, HEIGHT, FPS, TITLE
from boat import Boat
from player import Player
from level import Level
from ui import UI
from missions import AUFGABEN


class Game:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()

        self.ui = UI(WIDTH, HEIGHT)

        self.current_level = 1

        self.level = Level(self.current_level)

        self.player = Player()

        self.selected_cat = None
        self.cat_menu_open = False
        self.cat_message = ""

        self.message = ""
        self.message_timer = 0

        self.game_state = "intro"

        self.title_font = pygame.font.Font(None, 48)

        self.font = pygame.font.Font(None, 26)

        self.lives = 3

        self.invincible = False
        self.invincible_timer = 0

        self.cooldown = 0

        self.heart_image = pygame.image.load("assets/hp.PNG").convert_alpha()

        self.heart_image = pygame.transform.scale(self.heart_image, (40, 40))

        self.water_tiles = [
            pygame.transform.scale(pygame.image.load("assets/waterbig1.PNG").convert(), (WIDTH, HEIGHT)),
            pygame.transform.scale(pygame.image.load("assets/waterbig2.PNG").convert(), (WIDTH, HEIGHT)),
            pygame.transform.scale(pygame.image.load("assets/waterbig3.PNG").convert(), (WIDTH, HEIGHT)),
            pygame.transform.scale(pygame.image.load("assets/waterbig4.PNG").convert(), (WIDTH, HEIGHT)),
        ]

        self.current_water = 0
        self.water_timer = 0

        self.scroll_image = pygame.image.load("assets/cat_info.PNG").convert_alpha()

        self.scroll_image = pygame.transform.scale(self.scroll_image, (800, 900))

        self.scroll_rect = self.scroll_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def intro(self):

        self.screen.blit(self.scroll_image, self.scroll_rect)

        title_font = pygame.font.Font(None, 42)
        text_font = pygame.font.Font(None, 25)
        small_font = pygame.font.Font(None, 22)

        center_x = self.scroll_rect.centerx

        title = title_font.render("NYAN CAT: The Arc", True, (70, 45, 25))

        title_rect = title.get_rect(center=(center_x, self.scroll_rect.top + 280))

        self.screen.blit(title, title_rect)

        lines = [
            "",
            "",
            "In der Welt der kleinen Katzen",
            "ist eine schreckliche Überschwemmung",
            "ausgebrochen.",
            "",
            "Das Wasser steigt immer weiter.",
            "Viele Katzen sitzen auf ihren Inseln fest.",
            "",
            "Du bist ein mutiger Katzenretter.",
            "Mit deinem Floß machst du dich auf den Weg,",
            "um die Katzen zu retten.",
        ]

        y = self.scroll_rect.top + 350

        for line in lines:

            if line == "":
                y += 12
                continue

            text = text_font.render(line, True, (70, 45, 25))

            text_rect = text.get_rect(center=(center_x, y))

            self.screen.blit(text, text_rect)

            y += 20

        warning = text_font.render("ACHTUNG!", True, (150, 60, 30))

        warning_rect = warning.get_rect(center=(center_x, y + 20))

        self.screen.blit(warning, warning_rect)

        warning_text = small_font.render("Auf deinem Weg gibt es Hindernisse.", True, (70, 45, 25))

        warning_text_rect = warning_text.get_rect(center=(center_x, y + 50))

        self.screen.blit(warning_text, warning_text_rect)

        lives_text = small_font.render("Du hast nur 3 Leben!", True, (70, 45, 25))

        lives_rect = lives_text.get_rect(center=(center_x, y + 77))

        self.screen.blit(lives_text, lives_rect)

        enter = text_font.render("ENTER - Weiter", True, (70, 120, 50))

        enter_rect = enter.get_rect(center=(center_x, self.scroll_rect.bottom - 165))

        self.screen.blit(enter, enter_rect)

    def mission(self):

        self.draw_water()
        self.level.draw(self.screen)
        self.player.draw(self.screen)
        self.screen.blit(self.scroll_image, self.scroll_rect)
        title_font = pygame.font.Font(None, 42)
        text_font = pygame.font.Font(None, 25)

        center_x = self.scroll_rect.centerx

        mission = AUFGABEN[self.current_level]

        title = title_font.render(mission["lev_aufgaben"],True,(70, 45, 25))
        title_rect = title.get_rect(center=(center_x, self.scroll_rect.top + 280))
        self.screen.blit(title, title_rect)
        lines = mission["aufgabe"]

        y = self.scroll_rect.top + 400

        for line in lines:

            if line == "":
                y += 12
                continue

            color = (150, 60, 30) if line == "ACHTUNG!" else (70, 45, 25)

            text = text_font.render(line, True, color)

            text_rect = text.get_rect(center=(center_x, y))

            self.screen.blit(text, text_rect)

            y += 27
        enter = text_font.render("ENTER - Spiel starten", True, (70, 120, 50))
        enter_rect = enter.get_rect(center=(center_x, self.scroll_rect.bottom - 165))
        self.screen.blit(enter, enter_rect)


    def draw_water(self):
        self.screen.blit(self.water_tiles[self.current_water], (0, 0))

    def next_level(self):
        if self.current_level >= 5:
            self.game_state = "game_won"
            return

        self.current_level += 1
        self.player.boat.upgrade()
        self.level = Level(self.current_level)

        spawn_x, spawn_y = self.level.level_spawn[self.current_level]

        self.player.x = spawn_x
        self.player.y = spawn_y

        self.player.rect.x = int(self.player.x)
        self.player.rect.y = int(self.player.y)

        self.player.boat.x = self.player.x
        self.player.boat.y = self.player.y + 50
        self.player.boat.rect.center = (int(self.player.boat.x), int(self.player.boat.y))

        self.selected_cat = None
        self.cat_menu_open = False
        self.cat_message = ""

        self.lives = 3
        self.cooldown = 0
        self.invincible = False
        self.invincible_timer = 0

        self.game_state = "mission"

    def restart_level(self):
        self.level = Level(self.current_level)

        spawn_x, spawn_y = self.level.level_spawn[self.current_level]
        self.player.x = spawn_x
        self.player.y = spawn_y
        self.player.rect.x = int(self.player.x)
        self.player.rect.y = int(self.player.y)
        self.player.boat.x = self.player.x
        self.player.boat.y = self.player.y + 50
        self.player.boat.rect.center = (int(self.player.boat.x), int(self.player.boat.y))
        self.selected_cat = None
        self.cat_menu_open = False
        self.cat_message = ""
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
        self.cooldown = 0
        self.game_state = "playing"

    def draw_game_won(self):

        self.draw_water()

        font_big = pygame.font.Font(None, 60)

        font_small = pygame.font.Font(None, 30)

        title = font_big.render("DU HAST GEWONNEN!", True, (70, 120, 50))

        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

        self.screen.blit(title, title_rect)

        text = font_small.render("Alle 5 Level abgeschlossen!", True, (70, 45, 25))

        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))

        self.screen.blit(text, text_rect)

        enter = font_small.render("ENTER - Beenden", True, (70, 120, 50))

        enter_rect = enter.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))

        self.screen.blit(enter, enter_rect)

    def run(self):

        self.running = True

        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if self.game_state == "intro":

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_RETURN:
                            self.game_state = "mission"

                    continue

                if self.game_state == "mission":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.game_state = "playing"
                    continue

                if self.game_state == "level_complete":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.next_level()
                    continue

                if self.game_state == "game_over":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.restart_level()
                    continue
                if self.game_state == "game_won":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.running = False
                    continue
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.cat_menu_open = False
                        self.selected_cat = None
                        self.cat_message = ""
                    elif event.key == pygame.K_e:
                        if self.cat_menu_open:
                            if self.selected_cat:
                                success = self.level.take_cat(self.selected_cat, self.player.boat)
                                if success:
                                    self.cat_message = "Katze aufgenommen!"

                                    self.selected_cat = None
                                    self.cat_menu_open = False

                                else:

                                    self.cat_message = "Floß ist voll!"

                        else:

                            if self.level.finishlev(self.player.boat):

                                if self.level.check_mission(self.player.boat):

                                    self.game_state = "level_complete"

                                else:

                                    self.game_state = "game_over"

                            else:

                                cat = self.level.get_nearby_cat(self.player.boat)

                                if cat:
                                    self.selected_cat = cat
                                    self.cat_menu_open = True
                                    self.cat_message = ""

            if self.game_state == "intro":
                self.draw_water()

                self.level.draw(self.screen)

                self.player.draw(self.screen)

                self.intro()

                pygame.display.flip()

                self.clock.tick(FPS)

                continue

            if self.game_state == "mission":
                self.draw_water()

                self.level.draw(self.screen)

                self.player.draw(self.screen)

                self.mission()

                self.ui.draw_hearts(self.screen, self.lives)

                pygame.display.flip()

                self.clock.tick(FPS)

                continue

            if self.game_state == "level_complete":
                self.draw_water()

                self.level.draw(self.screen)

                self.player.draw(self.screen)

                self.ui.draw_level_complete(self.screen)

                pygame.display.flip()

                self.clock.tick(FPS)

                continue

            if self.game_state == "game_over":
                self.draw_water()

                self.level.draw(self.screen)

                self.player.draw(self.screen)

                self.ui.draw_game_over(self.screen)

                pygame.display.flip()

                self.clock.tick(FPS)

                continue

            if self.game_state == "game_won":
                self.draw_game_won()

                pygame.display.flip()

                self.clock.tick(FPS)

                continue

            if self.water_timer > 800:
                self.water_timer = 0

                self.current_water = (self.current_water + 1) % len(self.water_tiles)

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

            if self.cooldown > 0:
                self.cooldown -= 1

            if self.level.check_obstacle_collision(self.player.boat):

                self.player.x = old_x
                self.player.y = old_y

                self.player.rect.x = int(self.player.x)

                self.player.rect.y = int(self.player.y)

                if self.cooldown == 0:

                    self.lives -= 1

                    self.cooldown = 60

                    if self.lives == 0:
                        self.game_state = "game_over"

            if self.invincible:

                self.invincible_timer -= 1

                if self.invincible_timer <= 0:
                    self.invincible = False

            self.draw_water()

            self.level.draw(self.screen)

            self.player.draw(self.screen)

            if self.cat_menu_open and self.selected_cat:
                self.ui.draw_cat_info(self.screen, self.selected_cat, self.cat_message)

            self.ui.draw_hearts(self.screen, self.lives)

            if self.message_timer > 0:

                self.message_timer -= 1

            else:
                self.message = ""

            if self.message:
                message_surface = self.ui.font.render(self.message, True, (255, 255, 255))

                message_rect = message_surface.get_rect(center=(WIDTH // 2, 100))

                pygame.draw.rect(self.screen, (40, 40, 40), message_rect.inflate(40, 20))

                self.screen.blit(message_surface, message_rect)

            pygame.display.flip()

            self.water_timer += self.clock.get_time()

            self.clock.tick(FPS)

        pygame.quit()
