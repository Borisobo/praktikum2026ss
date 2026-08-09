import pygame


class UI:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 42)

    def draw_cat_info(self, screen, cat):

        # Hintergrund des Menüs
        menu_rect = pygame.Rect(
            550,
            250,
            800,
            500
        )

        pygame.draw.rect(
            screen,
            (30, 30, 40),
            menu_rect
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            menu_rect,
            3
        )

        info = cat.get_info()

        # Name
        name_text = self.big_font.render(
            info["name"],
            True,
            (255, 255, 255)
        )

        screen.blit(
            name_text,
            (600, 290)
        )

        # Beruf
        beruf_text = self.font.render(
            "Beruf: " + info["beruf"],
            True,
            (255, 255, 255)
        )

        screen.blit(
            beruf_text,
            (600, 350)
        )

        # Bewertung
        rating_text = self.font.render(
            "Bewertung: " + str(info["rating"]),
            True,
            (255, 255, 255)
        )

        screen.blit(
            rating_text,
            (600, 400)
        )

        # Eigenschaften
        qualities = ", ".join(info["qualities"])

        qualities_text = self.font.render(
            "Eigenschaften: " + qualities,
            True,
            (255, 255, 255)
        )

        screen.blit(
            qualities_text,
            (600, 450)
        )

        # Hinweis
        take_text = self.font.render(
            "E - Katze aufnehmen",
            True,
            (100, 255, 100)
        )

        screen.blit(
            take_text,
            (600, 550)
        )

        cancel_text = self.font.render(
            "ESC - Schließen",
            True,
            (255, 255, 255)
        )

        screen.blit(
            cancel_text,
            (600, 600)
        )
