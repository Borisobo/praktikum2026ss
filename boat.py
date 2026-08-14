import pygame


BOAT_LEVELS = {
    1: {"max_cats": 3, "speed": 3.0, "upgrade_cost": 10, "image": "assets/boats/boat1.png"},
    2: {"max_cats": 7, "speed": 3.5, "upgrade_cost": 20, "image": "assets/boats/boat2.png"},
    3: {"max_cats": 11, "speed": 4.0, "upgrade_cost": 35, "image": "assets/boats/boat3.png"},
    4: {"max_cats": 15, "speed": 4.5, "upgrade_cost": 50, "image": "assets/boats/boat4.png"},
    5: {"max_cats": 19, "speed": 5.0, "upgrade_cost": None, "image": "assets/boats/boat5.png"}
}


class Boat:
    def __init__(self, x, y, level=1):
        self.level = level
        self.current_cats = []
        self.x = float(x)
        self.y = float(y)
        self.load_level()

    def load_level(self):
        stats = BOAT_LEVELS[self.level]

        self.max_cats = stats["max_cats"]
        self.speed = stats["speed"]
        self.upgrade_cost = stats["upgrade_cost"]

        image = pygame.image.load(stats["image"]).convert_alpha()
        image = image.subsurface(image.get_bounding_rect()).copy()

        width = 180 + (self.level - 1) * 55
        height = 130 + (self.level - 1) * 40

        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self.mask = pygame.mask.from_surface(self.image)

    def upgrade(self):
        if self.level >= 5:
            return False

        self.level += 1
        self.load_level()
        return True

    def has_free_space(self):
        return len(self.current_cats) < self.max_cats

    def add_cat(self, cat):
        if not self.has_free_space():
            return False

        self.current_cats.append(cat)
        return True

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        if self.level <= 2:
            y, x = 25, 0
        elif self.level == 3:
            y, x = 65, 0
        elif self.level == 4:
            y, x = 85, 0
        else:
            y, x = 115, 15

        for i, cat in enumerate(self.current_cats):
            row, col = divmod(i, 10)

            cat_x = self.rect.x + 15 + x + col * 17
            cat_y = self.rect.y + y + row * 25

            screen.blit(cat._image, (cat_x, cat_y))
