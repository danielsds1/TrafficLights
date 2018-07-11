import random
from background import *
from pygame import *
from pygame.sprite import *

CAR_LANES = [(WIDTH, int(HEIGHT / 2 - 3 * STREET / 8)),
             (WIDTH, int(HEIGHT / 2 - STREET / 8)),
             (0, int(HEIGHT / 2 + STREET / 8)),
             (0, int(HEIGHT / 2 + 3 * STREET / 8)),
             (int(WIDTH / 2 - 3 * STREET / 8), 0),
             (int(WIDTH / 2 - STREET / 8), 0),
             (int(WIDTH / 2 + STREET / 8), HEIGHT),
             (int(WIDTH / 2 + 3 * STREET / 8), HEIGHT)]

class Cars(Sprite):

  def __init__(self, lane: int):
    self.max_speed=random.randint(3,6)
    self.speed = self.max_speed
    self.lane = lane
    if lane == 0 or lane == 1:
      self.origin = 'r'
      self.sign = -1

    elif lane == 2 or lane == 3:
      self.origin = 'l'
      self.sign = 1
    elif lane == 4 or lane == 5:
      self.origin = 'u'
      self.sign = 1
    else:
      self.origin = 'd'
      self.sign = -1
    Sprite.__init__(self)
    self.image = image.load('img/car/' + self.origin + 'car.png')
    self.x = int(CAR_LANES[lane][0])  # variable denoting x position of car
    self.y = int(CAR_LANES[lane][1])  # y position of car
    self.rect = self.image.get_rect(center=(self.x, self.y))  # used to place the car

    # car1.move(xp,signal_counter,car2)

  def move(self, signal, car_ahead):

    self.speed += 0.05
    if self.speed > self.max_speed:
      self.speed = self.max_speed
    if car_ahead is not None:

      if car_ahead.speed<self.speed and abs(self.x - car_ahead.x)<50 and self.lane<4:
        self.speed = car_ahead.speed
      if car_ahead.speed < self.speed and abs(self.y - car_ahead.y) < 50 and self.lane > 4:
        self.speed = car_ahead.speed

    if 0 <= self.lane <= 1:
      if signal != 2 or abs(self.x - (STOP_LANE[0][0] + STRIPE + 40)) > 5:
        if car_ahead is None or abs(self.x - car_ahead.x)>50:
          self.x += self.sign * self.speed
          self.rect.right = self.x
      else:
        self.speed=0

    elif 2 <= self.lane <= 3:
      if signal != 2 or abs(self.x - (STOP_LANE[1][0])) > 5:
        if car_ahead is None or abs(self.x - car_ahead.x)>50:
          self.x += self.sign * self.speed
          self.rect.right = self.x
      else:
        self.speed=0

    elif 4 <= self.lane <= 5:
      if signal != 2 or abs(self.y - (STOP_LANE[2][1] - 40)) > 5:
        if car_ahead is None or abs(self.y - car_ahead.y)>50:
          self.y += self.sign * self.speed
          self.rect.top = self.y
      else:
        self.speed = 0

    elif 6 <= self.lane <= 7:
      if signal != 2 or abs(self.y - (STOP_LANE[3][1] + STRIPE + 40)) > 5:
        if car_ahead is None or abs(self.y - car_ahead.y) > 50:
          self.y += self.sign * self.speed
          self.rect.bottom = self.y
      else:
        self.speed = 0
