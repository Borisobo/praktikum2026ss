import pygame
import random
import os
from cat_data_nps import Cats

class Cat:

  cats = []
  for file in os.listdir("assets/cats.nps"):
    image = pygame.image.load("assets/cats.nps" + file).covert_alpha()
    cats.append(image)
    cat = random.choice(cats)

  def __init__(self, image, name, rating, qualities):
    self._image = image
    self._name = name
    self._rating = rating
    self._qualities = qualities
    
    
