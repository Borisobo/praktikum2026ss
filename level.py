import pygame 
from settings import HEIGHT , WIDTH

class Level :
  def __init__(self) :
    self.width = WIDTH
    self.height = HEIGHT
    
  def check_boundaries(self, player):
        if player.rect.left < 0:
            player.rect.left = 0
        # Правая граница
        if player.rect.right > self.width:
            player.rect.right = self.width
        # Верхняя граница
        if player.rect.top < 0:
            player.rect.top = 0
        # Нижняя граница
        if player.rect.bottom > self.height:
            player.rect.bottom = self.height
        # Синхронизируем координаты
        player.x = player.rect.x
        player.y = player.rect.y
