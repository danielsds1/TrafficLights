import datetime
import os
import math as mt
import random
from logic import *
from car import *
from background import *
from watch import *
from signal import *
from pygame import *
from pygame.sprite import *
from traffic import *
from buttons import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()


if __name__ == '__main__':
  traffic()
