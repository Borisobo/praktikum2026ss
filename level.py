import pygame
from settings import HEIGHT, WIDTH
from islands import Island
from levels.level1 import islands as level1_islands, spawn as level1_spawn
from levels.level2 import islands as level2_islands, spawn as level2_spawn
from levels.level3 import islands as level3_islands, spawn as level3_spawn
from levels.level4 import islands as level4_islands, spawn as level4_spawn
from levels.level5 import islands as level5_islands, spawn as level5_spawn
from cat import Cat
from obstacles import Obstacle
from obstacles_data import OBSTACLES


class Level:
    def __init__(self, level_number=1):
        self.level_number = level_number
        self.width, self.height = WIDTH, HEIGHT

        self.level_spawn = {
            1: level1_spawn, 2: level2_spawn, 3: level3_spawn,
            4: level4_spawn, 5: level5_spawn
        }

        levels = {
            1: level1_islands, 2: level2_islands, 3: level3_islands,
            4: level4_islands, 5: level5_islands
        }

        if level_number not in levels:
            raise ValueError(f"Level {level_number} does not exist")

        self.islands = [
            Island(d["type"], d["image"], d["x"], d["y"], d["width"], d["height"])
            for d in levels[level_number]
        ]

        self.cats = []
        for island in self.islands:
            self.cats.extend(Cat.create_cat(level_number, island.type))

        self.obstacles = [
            Obstacle(d["image"], d["x"], d["y"], d["width"], d["height"])
            for d in OBSTACLES.get(level_number, [])
        ]

        self.catlocations = set()

        self.finish_flag = pygame.image.load(
            "assets/finishflag.png"
        ).convert_alpha()
        self.finish_flag = pygame.transform.scale(self.finish_flag, (100, 100))
        self.finish_flag_rect = self.finish_flag.get_rect(center=(400, 300))

    def check_boundaries(self, boat):
        boat.rect.clamp_ip(pygame.Rect(0, 0, self.width, self.height))
        boat.x, boat.y = boat.rect.x, boat.rect.y

    def draw(self, screen):
        for island in self.islands:
            island.draw(screen)
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        for cat in self.cats:
            cat.draw(screen)
        screen.blit(self.finish_flag, self.finish_flag_rect)

    def check_collision(self, boat):
        for island in self.islands:
            if boat.rect.colliderect(island.rect):
                offset = (
                    island.rect.x - boat.rect.x,
                    island.rect.y - boat.rect.y
                )
                if boat.mask.overlap(island.mask, offset):
                    return True
        return False

    def get_nearby_cat(self, boat):
        for cat in self.cats:
            if not cat.is_taken and boat.rect.colliderect(cat.rect.inflate(80, 80)):
                return cat
        return None

    def check_obstacle_collision(self, boat):
        for obstacle in self.obstacles:
            if boat.rect.colliderect(obstacle.rect):
                offset = (
                    obstacle.rect.x - boat.rect.x,
                    obstacle.rect.y - boat.rect.y
                )
                if boat.mask.overlap(obstacle.mask, offset):
                    return True
        return False

    def take_cat(self, cat, boat):
        if boat.add_cat(cat):
            cat.take()
            self.catlocations.add(cat._location)
            return True
        return False

    def finishlev(self, boat):
        return boat.rect.colliderect(self.finish_flag_rect)

    def check_mission(self, boat):
        cats = boat.current_cats
        if not cats:
            return False

        avg = sum(cat._rating for cat in cats) / len(cats)

        if self.level_number == 1:
            return len(cats) >= 2 and avg >= 4.1

        if self.level_number == 2:
            return (
                len(cats) >= 2 and avg >= 4.2
                and any(cat._beruf == "Lagerarbeiterin" for cat in cats)
                and any(cat._beruf == "Bäckerin" for cat in cats)
            )

        if self.level_number == 3:
            return (
                avg >= 4.3
                and any(cat._beruf == "Handwerker" for cat in cats)
                and any(
                    "konzentriert" in cat._qualities or
                    "aufmerksam" in cat._qualities
                    for cat in cats
                )
            )

        if self.level_number == 4:
            return (
                len(cats) >= 3 and avg >= 4.4
                and any(cat._beruf == "Trainer" for cat in cats)
                and any(cat._beruf == "Kellnerin" for cat in cats)
                and any(cat._beruf == "Barista" for cat in cats)
            )

        if self.level_number == 5:
            return (
                avg >= 4.5
                and any(cat._beruf == "Bürgermeister" for cat in cats)
            )

        return False
