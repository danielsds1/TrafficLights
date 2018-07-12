def logic(via_p, clima, fluxo, via_s=2, use=True, num=1):
  if num==1:
    if via_p==2:
      if fluxo == 2 or fluxo == 1 and clima == 1:
        red_time = 20
        green_time = 30
      else:
        red_time = 9
        green_time = 20

    elif via_p == 0:
      if fluxo == 1 and clima == 0:
        red_time = 20
        green_time = 30
      else:
        red_time = 9
        green_time = 20

    elif via_p == 1:
      if fluxo == 0:
        red_time = 20
        green_time = 30
      if fluxo == 1 or fluxo == 2:
        red_time = 9
        green_time = 20

  elif num==2:
    if fluxo == 0:
      green_time = 27
      red_time = 30

    elif fluxo == 1:

      if via_p == 0:
        if clima == 0 and via_s == 0:
          green_time = 27
          red_time = 30
        else:
          green_time = 7
          red_time = 6

      elif via_p == 1:
        if clima == 0:
          green_time = 27;
          red_time = 30
        else:
          green_time = 14
          red_time = 9

      elif via_p == 2:
        if clima == 0:
          green_time = 14
          red_time = 9
        else:
          green_time = 27
          red_time = 30

    elif fluxo == 2:
      if via_p == 0:
        if clima == 0:
          green_time = 27
          red_time = 30
        else:
          green_time = 7
          red_time = 6
      else:
        green_time = 27
        red_time = 30

  else:
    green_time = 30
    red_time = 30
  return green_time, red_time
