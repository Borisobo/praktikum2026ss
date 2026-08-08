import pygame
import random
import os
from cat_data_nps import CATS

class Cat:

  cats = []
  for file in os.listdir("assets/cats.nps"):
    image = pygame.image.load("assets/cats.nps/" + file).covert_alpha()
    cats.append(image)

  def __init__(self, image, beruf, name, rating, qualities, location):
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
      image = cls.cats[0]

      cat = cls(image, cat_name["name"], cat_beruf["beruf"], cat_qualities["qualities"], cat_rating["rating"], cat_location["location"])

  
    
    
