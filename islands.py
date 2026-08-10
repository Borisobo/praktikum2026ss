import pygame

class Island:
    def __init__(self, island_type, image_path, x, y, width, height):
        # Typ der Insel
        self.type = island_type

        # Inselbild laden
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.mask = pygame.mask.from_surface(self.image)

        # Position der Insel
        self.rect = self.image.get_rect(topleft=(x, y))

        # Menüstatus
        self.menu_open = False

        # Zusätzliche Informationen der Insel
        self.data = {}

    # Insel zeichnen
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # Prüfen, ob der Spieler die Insel berührt
    def is_player_near(self, player):
        return self.rect.colliderect(player.rect)

    # Menü öffnen
    def open_menu(self):
        self.menu_open = True

    # Menü schließen
    def close_menu(self):
        self.menu_open = False
