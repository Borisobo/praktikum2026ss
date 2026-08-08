import pygame
import random
import os
from cat_data_nps import CATS

class Cat:

  cats = []
  for file in os.listdir("assets/cats.nps"):
    image = pygame.image.load("assets/cats.nps/" + file).covert_alpha()
    cats.append(image)

  def __init__(self, image, beruf, name, rating, qualities):
    self._image = image
    self._name = name
    self._rating = rating
    self._qualities = qualities
    self._beruf = beruf

  @classmethod
  def create_cat(cls, level, location):
    cat_objects = []
    for cat_data in CATS[level][location]:
      image = 

  
    
    
