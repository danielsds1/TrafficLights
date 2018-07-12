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
from buttons import *

# initialize pygame

CAPTION = 'Traffic Simulation'
FLOW = [50, 100, 200, 400]
MAX_CAR = [11, 5]
INTENSITY = [0, 1, 2, 3]
WEATHER = [1, 0.8]


def randLogic():
  MAX_GT = 30
  MIN_GT = 10
  MAX_RT = 30
  MIN_RT = 10
  green_time = random.randint(MIN_GT, MAX_GT)
  red_time = random.randint(MIN_RT, MAX_RT)
  return green_time, red_time


def traffic():
  clock = pygame.time.Clock()  # load clock

  viap = random.randint(0, 2)
  vias = random.randint(viap, 2)
  weather = random.randint(0, 1)
  flow = [random.randint(0, 1), random.randint(0, 1), random.randint(2, 3), random.randint(0, 1)]
  print(viap, vias, weather, flow)
  '''timeg = [0, 0, 0, 0]
  timer = [0, 0, 0, 0]
  export = {
    'viap': [0 for i in range(50)],
    'vias': [0 for i in range(50)],
    'weather': [0 for i in range(50)],
    'flow': [0 for i in range(50)],
    'timeg': [0 for i in range(50)],
    'timer': [0 for i in range(50)],
  }
  export['viap'][0] = viap
  export['vias'][0] = vias
  export['weather'][0] = weather
  export['flow'][0] = flow[0] + flow[1]'''

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

  carr = [[Cars(0, WEATHER[weather], viap), None], [Cars(1, WEATHER[weather], viap), None]]
  carl = [[Cars(2, WEATHER[weather], viap), None], [Cars(3, WEATHER[weather], viap), None]]
  caru = [[Cars(4, WEATHER[weather], vias), None], [Cars(5, WEATHER[weather], vias), None]]
  card = [[Cars(6, WEATHER[weather], vias), None], [Cars(7, WEATHER[weather], vias), None]]

  lsignal = Signal(SIGNAL_POS[0][0], SIGNAL_POS[0][1], 'l');
  lsignal.change_sign('green')
  rsignal = Signal(SIGNAL_POS[1][0], SIGNAL_POS[1][1], 'r');
  rsignal.change_sign('green')
  usignal = Signal(SIGNAL_POS[2][0], SIGNAL_POS[2][1], 'u');
  usignal.change_sign('red')
  dsignal = Signal(SIGNAL_POS[3][0], SIGNAL_POS[3][1], 'd');
  dsignal.change_sign('red')

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

  green_time, red_time = logic(viap, weather, flow[0] + flow[1], vias, True, 1)
  total_time = green_time + red_time + yellow_time
  rtime = 0
  #iter = 0

  while True:

    if rtime == 0:
      signal_counterv = 2
      usignal.change_sign('red')
      dsignal.change_sign('red')
      # if export['timeg'][iter] != 0:
      #  iter += 1
      #  viap = random.randint(0, 2)
      #  vias = random.randint(viap, 2)
      #  weather = random.randint(0, 1)
      #  flow = [random.randint(0, 1), random.randint(0, 1), random.randint(2, 3), random.randint(0, 1)]
      # export['viap'][iter] = viap
      # export['vias'][iter] = vias
      # export['weather'][iter] = weather
      # export['flow'][iter] = flow[0] + flow[1]
      # timeg = [0, 0, 0, 0]
      # timer = [0, 0, 0, 0]
      # print(iter-1, export['viap'][iter - 1],export['viap'][iter - 1], export['weather'][iter - 1], export['flow'][iter - 1], export['timeg'][iter - 1],              export['timer'][iter - 1])
    if rtime == 1:
      signal_counterh = 0
      lsignal.change_sign('green')
      rsignal.change_sign('green')
      usignal.change_sign('red')
      dsignal.change_sign('red')
    elif rtime == green_time + 1:
      signal_counterh = 1
      lsignal.change_sign('yellow')
      rsignal.change_sign('yellow')
    elif rtime == green_time + yellow_time:
      signal_counterh = 2
      lsignal.change_sign('red')
      rsignal.change_sign('red')
    elif rtime == green_time + yellow_time + 1:
      signal_counterv = 0
      usignal.change_sign('green')
      dsignal.change_sign('green')
    elif rtime == green_time + red_time + 1:
      signal_counterv = 1
      usignal.change_sign('yellow')
      dsignal.change_sign('yellow')
    #      export['timeg'][iter] = max(timeg)
    #      export['timer'][iter] = max(timer)

    if rtime < green_time + 1:
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
    elif rtime < green_time + yellow_time + 1:

      if cont != rtime:
        lwatch1.change_num('off')
        lwatch2.change_num('off')
        rwatch1.change_num('off')
        rwatch2.change_num('off')
      else:
        cont = rtime
    elif rtime < green_time + red_time + 1:
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
    seconds = (now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec) - (
      start.tm_hour * 3600 + start.tm_min * 60 + start.tm_sec)
    rtime = seconds % total_time
    mouse_pos = mouse.get_pos()
    click = mouse.get_pressed()

    drawBackground(frame)
    # print(frame.get_at((int(WIDTH/2),int(HEIGHT/2))))
    for i in range(len(carr)):
      for j in range(len(carr[i]) - 1):
        carr[i][j].move(signal_counterh, carr[i][j + 1])

    for i in range(len(carl)):
      for j in range(len(carl[i]) - 1):
        carl[i][j].move(signal_counterh, carl[i][j + 1])

    for i in range(len(caru)):
      for j in range(len(caru[i]) - 1):
        caru[i][j].move(signal_counterv, caru[i][j + 1])

    for i in range(len(card)):
      for j in range(len(card[i]) - 1):
        card[i][j].move(signal_counterv, card[i][j + 1])

    if carr[0][0] is None:
      carr[0].insert(0, Cars(0, WEATHER[weather], viap))
    if carr[0][0].x < WIDTH - 40 and len(carr[0]) < MAX_CAR[0] and random.randint(0, FLOW[INTENSITY[0]]) == 0:
      carr[0].insert(0, Cars(0, WEATHER[weather], viap))
    if carr[0][len(carr[0]) - 2].x < 0:
      carr[0].pop(len(carr[0]) - 2)

    if carr[1][0] is None:
      carr[1].insert(0, Cars(1, WEATHER[weather], viap))
    if carr[1][0].x < WIDTH - 40 and len(carr[1]) < MAX_CAR[0] and random.randint(0, FLOW[INTENSITY[0]]) == 0:
      carr[1].insert(0, Cars(1, WEATHER[weather], viap))
    if carr[1][len(carr[1]) - 2].x < 0:
      carr[1].pop(len(carr[1]) - 2)

    if carl[0][0] is None:
      carl[0].insert(0, Cars(2, WEATHER[weather], viap))
    if carl[0][0].x > 40 and len(carl[0]) < MAX_CAR[0] and random.randint(0, FLOW[INTENSITY[flow[0]]]) == 0:
      carl[0].insert(0, Cars(2, WEATHER[weather], viap))
    if carl[0][len(carl[0]) - 2].x > WIDTH:
      carl[0].pop(len(carl[0]) - 2)

    if carl[1][0] is None:
      carl[1].insert(0, Cars(3, WEATHER[weather], viap))
    if carl[1][0].x > 40 and len(carl[1]) < MAX_CAR[0] and random.randint(0, FLOW[INTENSITY[flow[1]]]) == 0:
      carl[1].insert(0, Cars(3, WEATHER[weather], viap))
    if carl[1][len(carl[1]) - 2].x > WIDTH:
      carl[1].pop(len(carl[1]) - 2)

    if caru[0][0] is None:
      caru[0].insert(0, Cars(4, WEATHER[weather], vias))
      # timeg[0] = rtime - green_time - yellow_time if timeg[0] == 0 else timeg[0]
    if caru[0][0].y > 40 and random.randint(0, FLOW[INTENSITY[flow[2]]]) == 0:
      if len(caru[0]) < MAX_CAR[1]:
        caru[0].insert(0, Cars(4, WEATHER[weather], vias))
      # else:
      # timer[0] = rtime if timer[0] == 0 else timer[0]
    if caru[0][len(caru[0]) - 2].y > HEIGHT:
      caru[0].pop(len(caru[0]) - 2)

    if caru[1][0] is None:
      caru[1].insert(0, Cars(5, WEATHER[weather], vias))
      # timeg[1] = rtime - green_time - yellow_time if timeg[1] == 0 else timeg[1]
    if caru[1][0].y > 40 and random.randint(0, FLOW[INTENSITY[flow[2]]]) == 0:
      if len(caru[1]) < MAX_CAR[1]:
        caru[1].insert(0, Cars(5, WEATHER[weather], vias))
      # else:
      # timer[1] = rtime if timer[1] == 0 else timer[1]
    if caru[1][len(caru[1]) - 2].y > HEIGHT:
      caru[1].pop(len(caru[1]) - 2)

    if card[0][0] is None:
      card[0].insert(0, Cars(6, WEATHER[weather], vias))
      # timeg[2] = rtime - green_time - yellow_time if timeg[2] == 0 else timeg[2]
    if card[0][0].y < WIDTH - 40 and random.randint(0, FLOW[INTENSITY[flow[3]]]) == 0:
      if len(card[0]) < MAX_CAR[1]:
        card[0].insert(0, Cars(6, WEATHER[weather], vias))
      # else:
      # timer[2] = rtime if timer[2] == 0 else timer[2]
    if card[0][len(card[0]) - 2].y < 0:
      card[0].pop(len(card[0]) - 2)

    if card[1][0] is None:
      card[1].insert(0, Cars(7, WEATHER[weather], vias))
      # timeg[3] = rtime - green_time - yellow_time if timeg[3] == 0 else timeg[3]
    if card[1][0].y < WIDTH - 40 and random.randint(0, FLOW[INTENSITY[3]]) == 0:
      if len(card[1]) < MAX_CAR[1]:
        card[1].insert(0, Cars(7, WEATHER[weather], vias))
      # else:
      # timer[3] = rtime if timer[3] == 0 else timer[3]
    if card[1][len(card[1]) - 2].y < 0:
      card[1].pop(len(card[1]) - 2)

    all_cars = Group(carr[0][:-1], carr[1][:-1], carl[0][:-1], carl[1][:-1], caru[0][:-1], caru[1][:-1], card[0][:-1],
                     card[1][:-1])
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
              try:
                green_time, red_time = logic()
                total_time = green_time + red_time + yellow_time
              except:
                green_time, red_time = randLogic()
                total_time = green_time + red_time + yellow_time
              break
          else:
            button2.hover('play')

          drawBackground(frame)
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
