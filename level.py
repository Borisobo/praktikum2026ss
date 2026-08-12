import pygame
# import random
from settings import HEIGHT, WIDTH
# from cat import Cat
# from resource import Resource
from islands import Island
from levels.level1 import islands
from cat import Cat
from boat import Boat
from cats_data_nps import CATS
from obstacles import Obstacle
from obstacles_data import OBSTACLES


class Level:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.islands = []
        for island_data in islands:
            self.islands.append(
                Island(
                    island_data["type"],
                    island_data["image"],
                    island_data["x"],
                    island_data["y"],
                    island_data["width"],
                    island_data["height"]
                )
            )
        self.cats = []
        self.catlocations = set()
        for island in self.islands:
            cats = Cat.create_cat(1, island.type)
            self.cats.extend(cats)

        self.obstacles = []
        self.finishflag_rect = pygame.Rect(1400, 700, 150, 150)
        for obstacle_data in OBSTACLES[1]:
            obstacle = Obstacle(
                obstacle_data["image"],
                obstacle_data["x"],
                obstacle_data["y"],
                obstacle_data["width"],
                obstacle_data["height"]
            )

            self.obstacles.append(obstacle)

        self.finish_flag = pygame.image.load("assets/finishflag.png").convert_alpha()

        self.finish_flag = pygame.transform.scale(self.finish_flag,(100, 100))
        self.finish_flag_rect = self.finish_flag.get_rect(center=(400, 300))



    # self.level_number = 1

    # self.islands = []

    # self.cats = []

    # self.resources = []

    # self.load_level()
    # def load_level(self):
    # if self.level_number == 1:
    # self.load_level_1()
    # def load_level_1(self):

    # self.islands.clear()

    # self.cats.clear()

    # self.resources.clear(
    def check_boundaries(self, boat):
        if boat.rect.left < 0:
            boat.rect.left = 0

        if boat.rect.right > self.width:
            boat.rect.right = self.width

        if boat.rect.top < 0:
            boat.rect.top = 0

        if boat.rect.bottom > self.height:
            boat.rect.bottom = self.height

        boat.x = boat.rect.x
        boat.y = boat.rect.y

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
                offset_x = island.rect.x - boat.rect.x
                offset_y = island.rect.y - boat.rect.y
                offset = (offset_x, offset_y)
                if boat.mask.overlap(island.mask, offset):
                    return True
        return False

    def get_nearby_cat(self, boat):
        for cat in self.cats:
            if cat.is_taken:
                continue
            if boat.rect.colliderect(cat.rect.inflate(80, 80)):
                return cat
        return None

    def check_obstacle_collision(self, boat):
        for obstacle in self.obstacles:
            if boat.rect.colliderect(obstacle.rect):
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
    def check_mission(self):
        resc = 0
        for cat in self.cats:
            if cat.is_taken:
                if cat._rating < 4.5:
                    return False
                resc += 1

        return resc >= 2
