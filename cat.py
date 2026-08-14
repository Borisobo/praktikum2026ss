import pygame
import os

from cats_data_nps import CATS


class Cat:

    cats = []

    def __init__(self, image, name, beruf, qualities, rating, location, level):
        self._image = image
        self._name = name
        self._beruf = beruf
        self._qualities = qualities
        self._rating = rating
        self._location = location
        self._level = level
        self.rect = self._image.get_rect(topleft=self._location)
        self.is_taken = False

    def get_info(self):
        return {
            "name": self._name,
            "beruf": self._beruf,
            "rating": self._rating,
            "qualities": self._qualities
        }

    @classmethod
    def create_cat(cls, level, location):

        if not cls.cats:
            files = sorted(os.listdir("assets/cats.nps"))

            for file in files:
                image = pygame.image.load(
                    "assets/cats.nps/" + file
                ).convert_alpha()

                image = pygame.transform.scale(
                    image,
                    (40, 50)
                )

                cls.cats.append(image)

        start_index = 0

        for island in CATS[level]:
            if island == location:
                break

            start_index += len(CATS[level][island])

        cat_objects = []

        for index, cat_data in enumerate(CATS[level][location]):

            image = cls.cats[start_index + index]

            cat = cls(
                image,
                cat_data["name"],
                cat_data["beruf"],
                cat_data["qualities"],
                cat_data["rating"],
                cat_data["location"],
                level
            )

            cat_objects.append(cat)

        return cat_objects

    def take(self):
        self.is_taken = True

    def draw(self, screen):
        if not self.is_taken:
            screen.blit(self._image, self.rect)
