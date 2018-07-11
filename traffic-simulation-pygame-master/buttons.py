from pygame import *
from pygame.sprite import *

BTN_POS = [[20, 20], [61, 20], [102, 20]]

class Button(Sprite):
  def __init__(self, button, x, y):
    Sprite.__init__(self)
    self.image = image.load('img/btn/' + button + '.png')
    self.rect = self.image.get_rect(center=(x, y))
  def hover(self, button):
    self.image = image.load('img/btn/' + button + '.png')
