import pygame
import random
import os
from cats_data_nps import CATS

class Cat:

  cats = []
  cat_index = 0
  for file in os.listdir("assets/cats.nps"):
    image = pygame.image.load("assets/cats.nps/" + file).convert_alpha()
    cats.append(image)

  def __init__(self, image, name, beruf, qualities, rating, location):
    self._image = image
    self._name = name
    self._beruf = beruf
    self._qualities = qualities
    self._rating = rating
    self._location = location
    
    

  @classmethod
  def create_cat(cls, level, location):
    cat_objects = []
    for cat_data in CATS[level][location]:
      image = cls.cats[cls.cat_index]
      cls.cat_index += 1

      cat = cls(image, cat_data["name"], cat_data["beruf"], cat_data["qualities"], cat_data["rating"], cat_data["location"])
      cat_objects.append(cat)
    return cat_objects

  
    
    
