from pygame import *
from pygame.sprite import *

class Signal(Sprite):
  def __init__(self, x, y, origin):
    Sprite.__init__(self)
    self.origin = origin
    self.image = image.load('img/lite/' + origin + 'red.png')
    self.rect = self.image.get_rect(center=(x, y))

  def change_sign(self, color):
    self.image = image.load('img/lite/' + self.origin + color + '.png')
