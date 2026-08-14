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
            for file in sorted(os.listdir("assets/cats.nps")):
                image = pygame.image.load("assets/cats.nps/" + file).convert_alpha()
                cls.cats.append(pygame.transform.scale(image, (40, 50)))

        start = sum(len(CATS[l][i]) for l in range(1, level) for i in CATS[l])

        for island in CATS[level]:
            if island == location:
                break
            start += len(CATS[level][island])

        return [
            cls(
                cls.cats[start + i],
                data["name"],
                data["beruf"],
                data["qualities"],
                data["rating"],
                data["location"],
                level
            )
            for i, data in enumerate(CATS[level][location])
        ]
    def take(self):
        self.is_taken = True

    def draw(self, screen):
        if not self.is_taken:
            screen.blit(self._image, self.rect)
