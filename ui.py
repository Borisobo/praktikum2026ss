import pygame


class UI:

    def __init__(self, screen_width, screen_height):

        # Bildschirmgröße speichern
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Schriftarten
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 26)
        self.title_font = pygame.font.Font(None, 42)

        # Zustand des Menüs
        self.cat_menu_open = False

        # Aktuell angezeigte Katze
        self.selected_cat = None

    def open_cat_menu(self, cat):

        # Katzenmenü öffnen
        self.cat_menu_open = True

        # Katze speichern
        self.selected_cat = cat

    def close_cat_menu(self):

        # Katzenmenü schließen
        self.cat_menu_open = False

        # Auswahl zurücksetzen
        self.selected_cat = None

    def draw_interaction_hint(self, screen):

        # Nur anzeigen, wenn keine Katze ausgewählt wurde
        if self.cat_menu_open:
            return

        text = self.font.render(
            "E - Mit Katze interagieren",
            True,
            (255, 255, 255)
        )

        rect = text.get_rect(
            center=(
                self.screen_width // 2,
                self.screen_height - 50
            )
        )

        # Hintergrund
        background = rect.inflate(30, 15)

        pygame.draw.rect(
            screen,
            (30, 30, 30),
            background,
            border_radius=8
        )

        screen.blit(text, rect)

    def draw_cat_menu(self, screen):

        if not self.cat_menu_open:
            return

        if self.selected_cat is None:
            return

        # Dunkler Hintergrund
        overlay = pygame.Surface(
            (self.screen_width, self.screen_height),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 140))

        screen.blit(
            overlay,
            (0, 0)
        )

        # Menügröße
        menu_width = 600
        menu_height = 450

        menu_x = (
            self.screen_width - menu_width
        ) // 2

        menu_y = (
            self.screen_height - menu_height
        ) // 2

        menu_rect = pygame.Rect(
            menu_x,
            menu_y,
            menu_width,
            menu_height
        )

        # Menü zeichnen
        pygame.draw.rect(
            screen,
            (40, 40, 40),
            menu_rect,
            border_radius=15
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            menu_rect,
            width=2,
            border_radius=15
        )

        cat = self.selected_cat

        # Name
        title = self.title_font.render(
            cat._name,
            True,
            (255, 255, 255)
        )

        screen.blit(
            title,
            (menu_x + 30, menu_y + 25)
        )

        # Beruf
        beruf = self.font.render(
            f"Beruf: {cat._beruf}",
            True,
            (220, 220, 220)
        )

        screen.blit(
            beruf,
            (menu_x + 30, menu_y + 85)
        )

        # Rating
        rating = self.font.render(
            f"Rating: {cat._rating}",
            True,
            (255, 220, 100)
        )

        screen.blit(
            rating,
            (menu_x + 30, menu_y + 125)
        )

        # Überschrift für Eigenschaften
        qualities_title = self.font.render(
            "Eigenschaften:",
            True,
            (255, 255, 255)
        )

        screen.blit(
            qualities_title,
            (menu_x + 30, menu_y + 175)
        )

        # Eigenschaften
        y = menu_y + 215

        for quality in cat._qualities:

            text = self.small_font.render(
                "• " + quality,
                True,
                (210, 210, 210)
            )

            screen.blit(
                text,
                (menu_x + 40, y)
            )

            y += 30

        # Bedienung
        action_text = self.small_font.render(
            "E - Katze aufnehmen",
            True,
            (255, 255, 255)
        )

        close_text = self.small_font.render(
            "ESC - Schließen",
            True,
            (255, 255, 255)
        )

        screen.blit(
            action_text,
            (menu_x + 30, menu_y + 370)
        )

        screen.blit(
            close_text,
            (menu_x + 350, menu_y + 370)
        )
