import pygame



BOAT_LEVELS = {
    1: {
        "max_cats": 2,
        "speed": 3.0,
        "upgrade_cost": 10,
        "image": "assets/boats/boat1.png"
    },
    2: {
        "max_cats": 4,
        "speed": 3.5,
        "upgrade_cost": 20,
        "image": "assets/boats/boat2.png"
    },
    3: {
        "max_cats": 6,
        "speed": 4.0,
        "upgrade_cost": 35,
        "image": "assets/boats/boat3.png"
    },
    4: {
        "max_cats": 8,
        "speed": 4.5,
        "upgrade_cost": 50,
        "image": "assets/boats/boat4.png"
    },
    5: {
        "max_cats": 10,
        "speed": 5.0,
        "upgrade_cost": None,
        "image": "assets/boats/boat5.png"
    }
}


class Boat:
    def __init__(self, x, y):
        self.level = 1
        self.current_cats = []

        self.x = float(x)
        self.y = float(y)


        self.load_level()

    def load_level(self):
        stats = BOAT_LEVELS[self.level]

        self.max_cats = stats["max_cats"]
        self.speed = stats["speed"]
        self.upgrade_cost = stats["upgrade_cost"]
        self.image = pygame.image.load(stats["image"]).convert_alpha()
        bounding = self.image.get_bounding_rect()
        self.image = self.image.subsurface(bounding).copy()

        self.image = pygame.transform.scale(self.image, (128, 100))

        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

        self.mask = pygame.mask.from_surface(self.image)

    def upgrade(self):
        if self.level < 5:
            self.level += 1
            self.load_level()

    def has_free_space(self):
        return len(self.current_cats) < self.max_cats

    def add_cat(self, cat):
        if self.has_free_space():
            self.current_cats.append(cat)
            return True
        return False

    def remove_cat(self, cat):
        if cat in self.current_cats:
            self.current_cats.remove(cat)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
