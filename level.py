import pygame 
#import random
from settings import HEIGHT , WIDTH
#from cat import Cat
#from resource import Resource
#from island import Island

class Level :
  def __init__(self) :
    self.width = WIDTH
    self.height = HEIGHT

   # self.level_number = 1

       # self.islands = []

        #self.cats = []

        #self.resources = []

        #self.load_level()
  #def load_level(self):
    #if self.level_number == 1:
        #self.load_level_1()
  #def load_level_1(self):

    #self.islands.clear()

    #self.cats.clear()

    #self.resources.clear(
  def check_boundaries(self, player):
        if player.rect.left < 0:
            player.rect.left = 0
      
        if player.rect.right > self.width:
            player.rect.right = self.width
        
        if player.rect.top < 0:
            player.rect.top = 0
        
        if player.rect.bottom > self.height:
            player.rect.bottom = self.height
          
        player.x = player.rect.x
        player.y = player.rect.y
