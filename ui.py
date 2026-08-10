from settings import WIDTH, HEIGHT
import pygame


class UI:

    def __init__(self, WIDTH, HEIGHT):

        self.width = WIDTH
        self.height = HEIGHT

        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 42)

    def draw_cat_info(self, screen, cat, message=""):
        scroll_image = pygame.image.load(
            "assets/cat_info.PNG"
        ).convert()
        # Размер свитка
        scroll_image = pygame.transform.scale(
            scroll_image,
            (700, 700)
        )

        scroll_rect = scroll_image.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)
        )

        screen.blit(
            scroll_image,
            scroll_rect
        )

        info = cat.get_info()

        center_x = scroll_rect.centerx



        name_text = self.big_font.render(
            info["name"],
            True,
            (70, 45, 25)
        )

        name_rect = name_text.get_rect(
            center=(center_x, scroll_rect.top + 175)
        )

        screen.blit(
            name_text,
            name_rect
        )


        beruf_text = self.font.render(
            "Beruf: " + info["beruf"],
            True,
            (70, 45, 25)
        )

        beruf_rect = beruf_text.get_rect(
            center=(center_x, scroll_rect.top + 235)
        )

        screen.blit(
            beruf_text,
            beruf_rect
        )


        rating_text = self.font.render(
            "Bewertung: " + str(info["rating"]),
            True,
            (70, 45, 25)
        )

        rating_rect = rating_text.get_rect(
            center=(center_x, scroll_rect.top + 280)
        )

        screen.blit(
            rating_text,
            rating_rect
        )


        qualities = ", ".join(info["qualities"])

        qualities = ", ".join(info["qualities"])

        qualities_title = self.font.render(
            "Eigenschaften:",
            True,
            (70, 45, 25)
        )

        qualities_title_rect = qualities_title.get_rect(
            center=(center_x, scroll_rect.top + 330)
        )

        screen.blit(
            qualities_title,
            qualities_title_rect
        )

        qualities_text = self.font.render(
            qualities,
            True,
            (70, 45, 25)
        )

        qualities_rect = qualities_text.get_rect(
            center=(center_x, scroll_rect.top + 365)
        )

        screen.blit(
            qualities_text,
            qualities_rect
        )


        take_text = self.font.render(
            "E - Katze aufnehmen",
            True,
            (70, 120, 50)
        )

        take_rect = take_text.get_rect(
            center=(center_x, scroll_rect.bottom - 90)
        )

        screen.blit(
            take_text,
            take_rect
        )


        cancel_text = self.font.render(
            "ESC - Schließen",
            True,
            (100, 70, 40)
        )

        cancel_rect = cancel_text.get_rect(
            center=(center_x, scroll_rect.bottom - 55)
        )

        screen.blit(
            cancel_text,
            cancel_rect
        )

        if message:
            message_surface = self.font.render(
                message,
                True,
                (180, 50, 40)
            )

            message_rect = message_surface.get_rect(
                center=(center_x, scroll_rect.bottom - 25)
            )

            screen.blit(
                message_surface,
                message_rect
            )
