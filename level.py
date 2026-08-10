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
        for island in self.islands:
            cats = Cat.create_cat(1, island.type)
            self.cats.extend(cats)


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
            for cat in self.cats:
                cat.draw(screen)

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


    def take_cat(self, cat, boat):
        if cat._rating != 4.5:
            return False
        if boat.add_cat(cat):
            cat.take()
            return True

        return False
