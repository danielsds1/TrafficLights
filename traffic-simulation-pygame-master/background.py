from pygame import *
from pygame.sprite import *
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BGCOLOR = (128, 128, 128)

STREET = 120
STRIPE = 6
WIDTH = int(120 * 11)
HEIGHT = int(120 * 6)

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

def drawBackground(frame):
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
