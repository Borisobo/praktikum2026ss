import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
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
        self.level = Level(1)
        self.player = Player()

        self.selected_cat = None
        self.cat_menu_open = False
        self.cat_message = ""
        self.message = ""
        self.message_timer = 0
        self.game_state = "intro"

        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
        self.cooldown = 0

        self.water_tiles = [
            pygame.transform.scale(
                pygame.image.load(f"assets/waterbig{i}.PNG").convert(),
                (WIDTH, HEIGHT)
            )
            for i in range(1, 5)
        ]
        self.current_water = 0
        self.water_timer = 0

        self.scroll_image = pygame.image.load(
            "assets/cat_info.PNG"
        ).convert_alpha()
        self.scroll_image = pygame.transform.scale(
            self.scroll_image, (800, 900)
        )
        self.scroll_rect = self.scroll_image.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)
        )

    def intro(self):
        self.screen.blit(self.scroll_image, self.scroll_rect)
        title_font = pygame.font.Font(None, 42)
        text_font = pygame.font.Font(None, 25)
        small_font = pygame.font.Font(None, 22)
        center = self.scroll_rect.centerx

        title = title_font.render("NYAN CAT: The Arc", True, (70, 45, 25))
        self.screen.blit(
            title, title.get_rect(center=(center, self.scroll_rect.top + 280))
        )

        lines = [
            "",
            "",
            "In der Katzenwelt hat eine schreckliche",
            "Überschwemmung begonnen.",
            "Das Wasser steigt immer weiter und",
            "mehrere Katzen sitzen auf ihren Inseln fest.",
            "",
            "Unser Hauptheld Nyan Cat besitzt ein magisches Schiff.",
            "Mit seiner Hilfe kann er zwischen den Inseln fahren",
            "und mehrere Katzen vor der Überschwemmung retten.",
            "",
            "Doch das Schiff hat nur begrenzt Platz.",
            "Deshalb muss Nyan Cat sorgfältig auswählen,",
            "welche Katzen er mitnimmt.",
            "",
            "Hilf Nyan Cat, mehrere Katzen zu retten",
            "und sie an einen sicheren Ort zu bringen!"
        ]

        y = self.scroll_rect.top + 350
        for line in lines:
            if not line:
                y += 12
                continue
            text = text_font.render(line, True, (70, 45, 25))
            self.screen.blit(text, text.get_rect(center=(center, y)))
            y += 20

        for text, offset, color, font in [
            ("ACHTUNG!", 20, (150, 60, 30), text_font),
            ("Auf deinem Weg gibt es Hindernisse.", 50, (70, 45, 25), small_font),
            ("Du hast nur 3 Leben!", 77, (70, 45, 25), small_font),
            ("ENTER - Weiter", self.scroll_rect.bottom - self.scroll_rect.top - 165,
             (70, 120, 50), text_font)
        ]:
            surface = font.render(text, True, color)
            y_pos = y + offset if offset < 100 else self.scroll_rect.top + offset
            self.screen.blit(surface, surface.get_rect(center=(center, y_pos)))

    def mission(self):
        self.draw_water()
        self.level.draw(self.screen)
        self.player.draw(self.screen, self.current_level)
        self.screen.blit(self.scroll_image, self.scroll_rect)

        title_font = pygame.font.Font(None, 42)
        text_font = pygame.font.Font(None, 25)
        center = self.scroll_rect.centerx
        mission = AUFGABEN[self.current_level]

        title = title_font.render(
            mission["lev_aufgaben"], True, (70, 45, 25)
        )
        self.screen.blit(
            title, title.get_rect(center=(center, self.scroll_rect.top + 280))
        )

        y = self.scroll_rect.top + 400
        for line in mission["aufgabe"]:
            if not line:
                y += 12
                continue
            color = (150, 60, 30) if line == "ACHTUNG!" else (70, 45, 25)
            text = text_font.render(line, True, color)
            self.screen.blit(text, text.get_rect(center=(center, y)))
            y += 27

        text = text_font.render(
            "ENTER - Spiel starten", True, (70, 120, 50)
        )
        self.screen.blit(
            text,
            text.get_rect(center=(center, self.scroll_rect.bottom - 165))
        )

    def draw_water(self):
        self.screen.blit(self.water_tiles[self.current_water], (0, 0))

    def next_level(self):
        if self.current_level >= 5:
            self.game_state = "game_won"
            return

        self.current_level += 1
        self.player.boat.level = self.current_level
        self.player.boat.load_level()
        self.level = Level(self.current_level)

        x, y = self.level.level_spawn[self.current_level]
        self.player.x, self.player.y = x, y
        self.player.rect.topleft = (int(x), int(y))

        self.player.boat.x = x
        self.player.boat.y = y + 50
        self.player.boat.rect.center = (int(x), int(y + 50))

        self.selected_cat = None
        self.cat_menu_open = False
        self.cat_message = ""
        self.lives = 3
        self.cooldown = 0
        self.invincible = False
        self.invincible_timer = 0
        self.game_state = "mission"

    def restart_level(self):
        self.player.boat.current_cats = [
            cat for cat in self.player.boat.current_cats
            if cat._level != self.current_level
        ]

        self.level = Level(self.current_level)

        x, y = self.level.level_spawn[self.current_level]
        self.player.x, self.player.y = x, y
        self.player.rect.topleft = (int(x), int(y))

        self.player.boat.x = x
        self.player.boat.y = y + 50
        self.player.boat.rect.center = (int(x), int(y + 50))

        self.selected_cat = None
        self.cat_menu_open = False
        self.cat_message = ""
        self.lives = 3
        self.cooldown = 0
        self.invincible = False
        self.invincible_timer = 0
        self.game_state = "mission"

    def draw_game_won(self):
        self.draw_water()
        big = pygame.font.Font(None, 60)
        small = pygame.font.Font(None, 30)

        for text, y, font, color in [
            ("DU HAST GEWONNEN!", HEIGHT // 2 - 50, big, (70, 120, 50)),
            ("Alle 5 Level abgeschlossen!", HEIGHT // 2 + 20, small, (70, 45, 25)),
            ("ENTER - Beenden", HEIGHT // 2 + 80, small, (70, 120, 50))
        ]:
            surface = font.render(text, True, color)
            self.screen.blit(
                surface, surface.get_rect(center=(WIDTH // 2, y))
            )

    def run(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.game_state == "intro":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.game_state = "mission"
                    continue

                if self.game_state == "mission":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.game_state = "playing"
                    continue

                if self.game_state == "level_complete":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.next_level()
                    continue

                if self.game_state == "game_over":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.restart_level()
                    continue

                if self.game_state == "game_won":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.running = False
                    continue

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.cat_menu_open = False
                        self.selected_cat = None
                        self.cat_message = ""

                    elif event.key == pygame.K_e:
                        if self.cat_menu_open and self.selected_cat:
                            if self.level.take_cat(
                                self.selected_cat, self.player.boat
                            ):
                                self.cat_message = "Katze aufgenommen!"
                                self.selected_cat = None
                                self.cat_menu_open = False
                            else:
                                self.cat_message = "Floß ist voll!"

                        elif self.level.finishlev(self.player.boat):
                            self.game_state = (
                                "level_complete"
                                if self.level.check_mission(self.player.boat)
                                else "game_over"
                            )

                        else:
                            cat = self.level.get_nearby_cat(self.player.boat)
                            if cat:
                                self.selected_cat = cat
                                self.cat_menu_open = True
                                self.cat_message = ""

            if self.game_state == "intro":
                self.draw_water()
                self.level.draw(self.screen)
                self.player.draw(self.screen, self.current_level)
                self.intro()

            elif self.game_state == "mission":
                self.mission()
                self.ui.draw_hearts(self.screen, self.lives)

            elif self.game_state == "level_complete":
                self.draw_water()
                self.level.draw(self.screen)
                self.player.draw(self.screen, self.current_level)
                self.ui.draw_level_complete(self.screen)

            elif self.game_state == "game_over":
                self.draw_water()
                self.level.draw(self.screen)
                self.player.draw(self.screen, self.current_level)
                self.ui.draw_game_over(self.screen)

            elif self.game_state == "game_won":
                self.draw_game_won()

            else:
                if self.water_timer > 800:
                    self.water_timer = 0
                    self.current_water = (self.current_water + 1) % 4

                old_x, old_y = self.player.x, self.player.y
                self.player.update(pygame.key.get_pressed())
                self.level.check_boundaries(self.player)

                if self.level.check_collision(self.player.boat):
                    self.player.x, self.player.y = old_x, old_y
                    self.player.rect.topleft = (int(old_x), int(old_y))

                if self.cooldown > 0:
                    self.cooldown -= 1

                if self.level.check_obstacle_collision(self.player.boat):
                    self.player.x, self.player.y = old_x, old_y
                    self.player.rect.topleft = (int(old_x), int(old_y))

                    if self.cooldown == 0:
                        self.lives -= 1
                        self.cooldown = 60
                        if self.lives <= 0:
                            self.game_state = "game_over"

                self.draw_water()
                self.level.draw(self.screen)
                self.player.draw(self.screen, self.current_level)

                if self.cat_menu_open and self.selected_cat:
                    self.ui.draw_cat_info(
                        self.screen,
                        self.selected_cat,
                        self.cat_message
                    )

                self.ui.draw_hearts(self.screen, self.lives)

            pygame.display.flip()
            self.water_timer += self.clock.get_time()
            self.clock.tick(FPS)

        pygame.quit()
