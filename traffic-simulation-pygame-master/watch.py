from pygame import *
from pygame.sprite import *
class Watch(Sprite):
  def __init__(self, x, y):
    Sprite.__init__(self)
    self.image = image.load('img/num/off.png')
    self.rect = self.image.get_rect(center=(x, y))

  def change_num(self, num):
    self.image = image.load('img/num/' + str(num) + '.png')
