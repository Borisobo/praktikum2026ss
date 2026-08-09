import pygame 
from settings import HEIGHT , WIDTH
from cat import Cat
#from resource import Resource
from strand import Island

class Level :
  def __init__(self) :
    self.width = WIDTH
    self.height = HEIGHT
    self.islands = [
        Island(500, 300),
    ]


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

  def draw(self, screen):
      for island in self.islands:
          island.draw(screen)


  def check_collision(self, player):

      for island in self.islands:
          if player.rect.colliderect(island.rect):
              offset_x = island.rect.x - player.rect.x
              offset_y = island.rect.y - player.rect.y
              offset = (offset_x, offset_y)
              if player.mask.overlap(island.mask, offset):
                  return True
      return False
