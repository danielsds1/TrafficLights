import datetime
import os
import math as mt
import random
from pygame import *
from pygame.sprite import *

# initialize pygame
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BGCOLOR = (128, 128, 128)

STREET = 120
STRIPE = 6
WIDTH = int(120 * 11)
HEIGHT = int(120 * 6)

CAPTION = 'Traffic Simulation'
SPEED = 0
STREET_POS = [(0, (HEIGHT - STREET) / 2, WIDTH, STREET),
              ((WIDTH - STREET) / 2, 0, STREET, HEIGHT)]
SIGNAL_POS = [[WIDTH / 2 - STREET / 2 - 20, HEIGHT / 2 + STREET / 2 + 5],
              [WIDTH / 2 + STREET / 2 + 20, HEIGHT / 2 - STREET / 2 - 5],
              [WIDTH / 2 - STREET / 2 - 5, HEIGHT / 2 - STREET / 2 - 20],
              [WIDTH / 2 + STREET / 2 + 5, HEIGHT / 2 + STREET / 2 + 20]]

STOP_LANE = [(WIDTH / 2 + STREET * 5 / 4 - STRIPE, HEIGHT / 2 - STREET / 2, STRIPE, STREET),
             (WIDTH / 2 - STREET * 5 / 4, HEIGHT / 2 - STREET / 2, STRIPE, STREET),
             (WIDTH / 2 - STREET / 2, HEIGHT / 2 - STREET - 30, STREET, STRIPE),
             (WIDTH / 2 - STREET / 2, HEIGHT / 2 + STREET + 30 - STRIPE, STREET, STRIPE)]

DOUBLE_LANE = [(0, HEIGHT / 2 - 2, WIDTH / 2 - STREET * 5 / 4, STRIPE / 3),
               (0, HEIGHT / 2 + 2, WIDTH / 2 - STREET * 5 / 4, STRIPE / 3),
               (WIDTH / 2 + STREET * 5 / 4, HEIGHT / 2 - 2, WIDTH / 2 - STREET * 3 / 4, STRIPE / 3),
               (WIDTH / 2 + STREET * 5 / 4, HEIGHT / 2 + 2, WIDTH / 2 - STREET * 3 / 4, STRIPE / 3),
               (WIDTH / 2 - 2, 0, STRIPE / 3, HEIGHT / 2 - STREET * 5 / 4),
               (WIDTH / 2 + 2, 0, STRIPE / 3, HEIGHT / 2 - STREET * 5 / 4),
               (WIDTH / 2 - STRIPE / 3, HEIGHT / 2 + STREET + STREET / 4, STRIPE / 3, HEIGHT / 2 - STREET * 3 / 4),
               (WIDTH / 2 + STRIPE / 3, HEIGHT / 2 + STREET + STREET / 4, STRIPE / 3, HEIGHT / 2 - STREET * 3 / 4)]
DASHED_LANE = [(0, HEIGHT / 2 - STREET / 4, STRIPE * 2, STRIPE / 3),
               (0, HEIGHT / 2 + STREET / 4, STRIPE * 2, STRIPE / 3),
               (WIDTH / 2 + STREET * 5 / 4, HEIGHT / 2 - STREET / 4, STRIPE * 2, STRIPE / 3),
               (WIDTH / 2 + STREET * 5 / 4, HEIGHT / 2 + STREET / 4, STRIPE * 2, STRIPE / 3),
               (WIDTH / 2 - STREET / 4, 0, STRIPE / 3, STRIPE * 2),
               (WIDTH / 2 + STREET / 4, 0, STRIPE / 3, STRIPE * 2),
               (WIDTH / 2 - STREET / 4, HEIGHT / 2 + STREET * 5 / 4, STRIPE / 3, STRIPE * 2),
               (WIDTH / 2 + STREET / 4, HEIGHT / 2 + STREET * 5 / 4, STRIPE / 3, STRIPE * 2)]
CROSSWALK = [(WIDTH / 2 - STREET, (HEIGHT - STREET) / 2, STREET / 2, STRIPE),
             ((WIDTH + STREET) / 2, (HEIGHT - STREET) / 2, STREET / 2, STRIPE),
             ((WIDTH - STREET) / 2, HEIGHT / 2 - STREET, STRIPE, STREET / 2),
             ((WIDTH - STREET) / 2, (HEIGHT + STREET) / 2, STRIPE, STREET / 2)]
COUNT_POS = [(SIGNAL_POS[0][0] - 10, SIGNAL_POS[0][1] + 5, 20, 20),
             (SIGNAL_POS[1][0] - 10, SIGNAL_POS[1][1] - 25, 20, 20),
             (SIGNAL_POS[2][0] - 25, SIGNAL_POS[2][1] - 10, 20, 20),
             (SIGNAL_POS[3][0] + 5, SIGNAL_POS[3][1] - 10, 20, 20)]
CAR_LANES = [(WIDTH, int(HEIGHT / 2 - 3 * STREET / 8)),
             (WIDTH, int(HEIGHT / 2 - STREET / 8)),
             (0, int(HEIGHT / 2 + STREET / 8)),
             (0, int(HEIGHT / 2 + 3 * STREET / 8)),
             (int(WIDTH / 2 - 3 * STREET / 8), 0),
             (int(WIDTH / 2 - STREET / 8), 0),
             (int(WIDTH / 2 + STREET / 8), HEIGHT),
             (int(WIDTH / 2 + 3 * STREET / 8), HEIGHT)]
FLOW=[200,200,400,400]

CARSIZE = [40, 20]
BTN_POS = [[20, 20], [61, 20], [102, 20]]
MAX_CAR=[15,10]
velocity = [10, 10]


# make a class of cars
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

    #if self.x < 0 or self.x > WIDTH - 1:
    #  self.x = int(CAR_LANES[self.lane][0])
    #if self.y < 0 or self.y > HEIGHT - 1:
    #  self.y = int(CAR_LANES[self.lane][1])
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



class Signal(Sprite):
  def __init__(self, x, y, origin):
    Sprite.__init__(self)
    self.origin = origin
    self.image = image.load('img/lite/' + origin + 'red.png')
    self.rect = self.image.get_rect(center=(x, y))

  def change_sign(self, color):
    self.image = image.load('img/lite/' + self.origin + color + '.png')


class Watch(Sprite):
  def __init__(self, x, y):
    Sprite.__init__(self)
    self.image = image.load('img/num/off.png')
    self.rect = self.image.get_rect(center=(x, y))

  def change_num(self, num):
    self.image = image.load('img/num/' + str(num) + '.png')


class Button(Sprite):
  def __init__(self, button, x, y):
    Sprite.__init__(self)
    self.image = image.load('img/btn/' + button + '.png')
    self.rect = self.image.get_rect(center=(x, y))

  def hover(self, button):
    self.image = image.load('img/btn/' + button + '.png')

def logic():
  green_time='a'
  red_time='b'
  return green_time,red_time

def randLogic():
  MAX_GT=30
  MIN_GT=10
  MAX_RT=30
  MIN_RT=10
  green_time=random.randint(MIN_GT,MAX_GT)
  red_time=random.randint(MIN_RT,MAX_RT)
  return green_time,red_time

def drawBackground(frame, HEIGHT, WIDTH, STREET, STRIPE):
  frame.fill(BGCOLOR)

  # pygame.draw.rect(screen, color, (x,y,width,height), thickness)

  # Desenho das ruas
  pygame.draw.rect(frame, BLACK, STREET_POS[0], 0)
  pygame.draw.rect(frame, BLACK, STREET_POS[1], 0)

  # Desenho das faixas dupla contínuas na rua horizontal
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[0], 0)  # desenho da faixa contínua
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[1], 0)  # desenho da faixa contínua
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[2], 0)
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[3], 0)
  # Desenho das faixas dupla contínuas na rua vertical
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[4], 0)
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[5], 0)
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[6], 0)
  pygame.draw.rect(frame, YELLOW, DOUBLE_LANE[7], 0)

  # Desenho das faixas de retenção na rua horizontal
  pygame.draw.rect(frame, WHITE, STOP_LANE[0], 0)
  pygame.draw.rect(frame, WHITE, STOP_LANE[1], 0)
  # Desenho das faixas de retenção na rua horizontal
  pygame.draw.rect(frame, WHITE, STOP_LANE[2], 0)
  pygame.draw.rect(frame, WHITE, STOP_LANE[3], 0)

  # Desenho das faixas tracejadas
  for i in range(int((WIDTH / 2 - STREET) // (STRIPE * 4)) - 1):
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[0], (i * 4 * STRIPE, 0, 0, 0)))), 0)
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[1], (i * 4 * STRIPE, 0, 0, 0)))), 0)
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[2], (i * 4 * STRIPE, 0, 0, 0)))), 0)
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[3], (i * 4 * STRIPE, 0, 0, 0)))), 0)

  for i in range(int((HEIGHT / 2 - STREET) // (STRIPE * 4)) - 1):
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[4], (0, i * 4 * STRIPE, 0, 0)))), 0)
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[5], (0, i * 4 * STRIPE, 0, 0)))), 0)

    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[6], (0, i * 4 * STRIPE, 0, 0)))), 0)
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(DASHED_LANE[7], (0, i * 4 * STRIPE, 0, 0)))), 0)

    # Desenho das faixas de pedestres
  for i in range(10):
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(CROSSWALK[0], (0, i * STREET / 10, 0, 0)))), 0)
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(CROSSWALK[1], (0, i * STREET / 10, 0, 0)))), 0)

    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(CROSSWALK[2], (i * STREET / 10, 0, 0, 0)))), 0)
    pygame.draw.rect(frame, WHITE, tuple(map(sum, zip(CROSSWALK[3], (i * STREET / 10, 0, 0, 0)))), 0)

  # Desenho do background do contador

  pygame.draw.rect(frame, BLACK, COUNT_POS[0], 0)
  pygame.draw.rect(frame, BLACK, COUNT_POS[1], 0)
  pygame.draw.rect(frame, BLACK, COUNT_POS[2], 0)
  pygame.draw.rect(frame, BLACK, COUNT_POS[3], 0)


def traffic():
  clock = pygame.time.Clock()  # load clock
  # datetime.date.timetuple(datetime.datetime.now())
  # time.struct_time(tm_year=2018, tm_mon=7, tm_mday=4, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=2, tm_yday=185, tm_isdst=-1)
  start = datetime.datetime.timetuple(datetime.datetime.now())

  frame = pygame.display.set_mode((WIDTH, HEIGHT))
  display.set_caption(CAPTION)

  lwatch1 = Watch(SIGNAL_POS[0][0] - 5, SIGNAL_POS[0][1] + 15)
  lwatch2 = Watch(SIGNAL_POS[0][0] + 5, SIGNAL_POS[0][1] + 15)

  rwatch1 = Watch(SIGNAL_POS[1][0] - 5, SIGNAL_POS[1][1] - 15)
  rwatch2 = Watch(SIGNAL_POS[1][0] + 5, SIGNAL_POS[1][1] - 15)

  uwatch1 = Watch(SIGNAL_POS[2][0] - 20, SIGNAL_POS[2][1])
  uwatch2 = Watch(SIGNAL_POS[2][0] - 10, SIGNAL_POS[2][1])

  dwatch1 = Watch(SIGNAL_POS[3][0] + 10, SIGNAL_POS[3][1])
  dwatch2 = Watch(SIGNAL_POS[3][0] + 20, SIGNAL_POS[3][1])

  carr=[[Cars(0), None], [Cars(1), None]]
  carl=[[Cars(2), None], [Cars(3), None]]
  caru=[[Cars(4), None], [Cars(5), None]]
  card=[[Cars(6), None], [Cars(7), None]]

  lsignal = Signal(SIGNAL_POS[0][0], SIGNAL_POS[0][1], 'l'); lsignal.change_sign('green')
  rsignal = Signal(SIGNAL_POS[1][0], SIGNAL_POS[1][1], 'r'); rsignal.change_sign('green')
  usignal = Signal(SIGNAL_POS[2][0], SIGNAL_POS[2][1], 'u'); usignal.change_sign('red')
  dsignal = Signal(SIGNAL_POS[3][0], SIGNAL_POS[3][1], 'd'); dsignal.change_sign('red')

  button0 = Button('stop', BTN_POS[0][0], BTN_POS[0][1])
  button1 = Button('pause', BTN_POS[1][0], BTN_POS[1][1])
  button2 = Button('play', BTN_POS[2][0], BTN_POS[2][1])

  all_cars = Group(carr[0][:-1], carr[1][:-1], carl[0][:-1], carl[1][:-1], caru[0][:-1], caru[1][:-1], card[0][:-1],
                   card[1][:-1])
  all_signals = Group(lsignal, rsignal, usignal, dsignal)
  all_watches = Group(lwatch1, lwatch2, rwatch1, rwatch2, uwatch1, uwatch2, dwatch1, dwatch2)
  all_buttons = Group(button0, button1, button2)

  signal_counterh = 0
  signal_counterv = 2
  cont = 0
  yellow_time = 3
  try:
    green_time, red_time = logic()
    total_time = green_time + red_time + yellow_time
  except:
    green_time, red_time = randLogic()
    total_time = green_time + red_time + yellow_time
  rtime = 0

  while True:

    if rtime == 0:
      signal_counterv = 2
      usignal.change_sign('red')
      dsignal.change_sign('red')
    if rtime == 1:
      signal_counterh = 0
      lsignal.change_sign('green')
      rsignal.change_sign('green')
      usignal.change_sign('red')
      dsignal.change_sign('red')
    elif rtime == green_time+1:
      signal_counterh = 1
      lsignal.change_sign('yellow')
      rsignal.change_sign('yellow')
    elif rtime == green_time + yellow_time:
      signal_counterh = 2
      lsignal.change_sign('red')
      rsignal.change_sign('red')
    elif rtime == green_time + yellow_time+1:
      signal_counterv = 0
      usignal.change_sign('green')
      dsignal.change_sign('green')
    elif rtime == green_time + red_time+1:
      signal_counterv = 1
      usignal.change_sign('yellow')
      dsignal.change_sign('yellow')

    if rtime < green_time+1:
      if cont != rtime:
        lwatch1.change_num(mt.floor((green_time - rtime) / 10))
        lwatch2.change_num(mt.floor((green_time - rtime) % 10))
        rwatch1.change_num(mt.floor((green_time - rtime) / 10))
        rwatch2.change_num(mt.floor((green_time - rtime) % 10))
        uwatch1.change_num('off')
        uwatch2.change_num('off')
        dwatch1.change_num('off')
        dwatch2.change_num('off')
      else:
        cont = rtime
    elif rtime < green_time + yellow_time+1:

      if cont != rtime:
        lwatch1.change_num('off')
        lwatch2.change_num('off')
        rwatch1.change_num('off')
        rwatch2.change_num('off')
      else:
        cont = rtime
    elif rtime < green_time + red_time+1:
      if cont != rtime:

        lwatch1.change_num('off')
        lwatch2.change_num('off')
        rwatch1.change_num('off')
        rwatch2.change_num('off')
        uwatch1.change_num(mt.floor((green_time + red_time - rtime) / 10))
        uwatch2.change_num(mt.floor((green_time + red_time - rtime) % 10))
        dwatch1.change_num(mt.floor((green_time + red_time - rtime) / 10))
        dwatch2.change_num(mt.floor((green_time + red_time - rtime) % 10))
      else:
        cont = rtime
    else:
      uwatch1.change_num('off')
      uwatch2.change_num('off')
      dwatch1.change_num('off')
      dwatch2.change_num('off')
    now = datetime.datetime.timetuple(datetime.datetime.now())
    seconds = (now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec) - (start.tm_hour * 3600 + start.tm_min * 60 + start.tm_sec)
    rtime = seconds % total_time
    mouse_pos = mouse.get_pos()
    click = mouse.get_pressed()

    drawBackground(frame, HEIGHT, WIDTH, STREET, STRIPE)
    # print(frame.get_at((int(WIDTH/2),int(HEIGHT/2))))
    for i in range(len(carr)):
      for j in range(len(carr[i])-1):
        carr[i][j].move(signal_counterh, carr[i][j+1])

    for i in range(len(carl)):
      for j in range(len(carl[i])-1):
        carl[i][j].move(signal_counterh, carl[i][j + 1])

    for i in range(len(caru)):
      for j in range(len(caru[i])-1):
        caru[i][j].move(signal_counterv, caru[i][j + 1])

    for i in range(len(card)):
      for j in range(len(card[i])-1):
        card[i][j].move(signal_counterv, card[i][j + 1])

    if carr[0][0] is None:
      carr[0].insert(0, Cars(0))
    if carr[0][0].x < WIDTH-40 and len(carr[0]) < MAX_CAR[0] and random.randint(0, FLOW[0]) == 0:
      carr[0].insert(0, Cars(0))
    if carr[0][len(carr[0])-2].x < 0:
      carr[0].pop(len(carr[0])-2)

    if carr[1][0] is None:
      carr[1].insert(0, Cars(1))
    if carr[1][0].x < WIDTH-40 and len(carr[1]) < MAX_CAR[0] and random.randint(0, FLOW[0]) == 0:
      carr[1].insert(0, Cars(1))
    if carr[1][len(carr[1])-2].x < 0:
      carr[1].pop(len(carr[1])-2)

    if carl[0][0] is None:
      carl[0].insert(0, Cars(2))
    if carl[0][0].x > 40 and len(carl[0]) < MAX_CAR[0] and random.randint(0, FLOW[1]) == 0:
      carl[0].insert(0, Cars(2))
    if carl[0][len(carl[0])-2].x > WIDTH:
      carl[0].pop(len(carl[0])-2)

    if carl[1][0] is None:
      carl[1].insert(0, Cars(3))
    if carl[1][0].x > 40 and len(carl[1]) < MAX_CAR[0] and random.randint(0, FLOW[1]) == 0:
      carl[1].insert(0, Cars(3))
    if carl[1][len(carl[1])-2].x > WIDTH:
      carl[1].pop(len(carl[1])-2)

    if caru[0][0] is None:
      caru[0].insert(0, Cars(4))
    if caru[0][0].y > 40 and len(caru[0]) < MAX_CAR[1] and random.randint(0, FLOW[2]) == 0:
      caru[0].insert(0, Cars(4))
    if caru[0][len(caru[0])-2].y > HEIGHT:
      caru[0].pop(len(caru[0])-2)

    if caru[1][0] is None:
      caru[1].insert(0, Cars(5))
    if caru[1][0].y > 40 and len(caru[1]) < MAX_CAR[1] and random.randint(0, FLOW[2]) == 0:
      caru[1].insert(0, Cars(5))
    if caru[1][len(caru[1])-2].y > HEIGHT:
      caru[1].pop(len(caru[1])-2)

    if card[0][0] is None:
      card[0].insert(0, Cars(6))
    if card[0][0].y < WIDTH - 40 and len(card[0]) < MAX_CAR[1] and random.randint(0, FLOW[3]) == 0:
      card[0].insert(0, Cars(6))
    if card[0][len(card[0])-2].y < 0:
      card[0].pop(len(card[0])-2)

    if card[1][0] is None:
      card[1].insert(0, Cars(7))
    if card[1][0].y < WIDTH - 40 and len(card[1]) < MAX_CAR[1] and random.randint(0, FLOW[3]) == 0:
      card[1].insert(0, Cars(7))
    if card[1][len(card[1])-2].y < 0:
      card[1].pop(len(card[1])-2)



    all_cars = Group(carr[0][:-1], carr[1][:-1], carl[0][:-1], carl[1][:-1],caru[0][:-1], caru[1][:-1],card[0][:-1], card[1][:-1])
    e = event.pump()  # Don't ever remove this for Odin's sake!

    # Stop execution
    if BTN_POS[0][0] + 18 > mouse_pos[0] > BTN_POS[0][0] - 18 and BTN_POS[0][1] + 18 > mouse_pos[1] > BTN_POS[0][
      1] - 18:
      button0.hover('stoph')
      if click[0] == 1:
        break
    else:
      button0.hover('stop')
    # Pause execution
    if BTN_POS[1][0] + 18 > mouse_pos[0] > BTN_POS[1][0] - 18 and BTN_POS[1][1] + 18 > mouse_pos[1] > BTN_POS[1][
      1] - 18:
      button1.hover('pauseh')
      if click[0] == 1:
        while True:
          mouse_pos = mouse.get_pos()
          click = mouse.get_pressed()

          e = event.pump()  # Don't ever remove this for Odin's sake!
          if BTN_POS[0][0] + 18 > mouse_pos[0] > BTN_POS[0][0] - 18 and BTN_POS[0][1] + 18 > mouse_pos[1] > BTN_POS[0][
            1] - 18:
            button0.hover('stoph')
            if click[0] == 1:
              pygame.quit()
              quit()
          else:
            button0.hover('stop')
          if BTN_POS[2][0] + 18 > mouse_pos[0] > BTN_POS[2][0] - 18 and BTN_POS[2][1] + 18 > mouse_pos[1] > BTN_POS[2][
            1] - 18:
            button2.hover('playh')
            if click[0] == 1:
              button2.hover('play')
              start = datetime.datetime.timetuple(datetime.datetime.now())
              green_time, red_time = logic()
              total_time = green_time + red_time + yellow_time
              break
          else:
            button2.hover('play')

          drawBackground(frame, HEIGHT, WIDTH, STREET, STRIPE)
          all_cars.draw(frame)
          all_signals.draw(frame)
          all_watches.draw(frame)
          all_buttons.draw(frame)
          display.update()
          pygame.display.flip()
    else:
      button1.hover('pause')
    all_cars.draw(frame)
    all_signals.draw(frame)
    all_watches.draw(frame)
    all_buttons.draw(frame)
    display.update()
    pygame.display.flip()
  pygame.quit()
  quit()
  clock = pygame.time.Clock()  # load clock


if __name__ == '__main__':
  traffic()
