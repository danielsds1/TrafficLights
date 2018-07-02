# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 16:05:40 2018

@author: Daniel
"""

import sys, pygame, random, time
pygame.init()

size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

done = False

Black=0,0,0
White=255,255,255

Time = 0
Minute = 0
Hour = 0
Day = 0

#Fonts
Font = pygame.font.SysFont("Trebuchet MS", 25)

#Day
DayFont = Font.render("Day:"+str(Day),1, Black)
DayFontR=DayFont.get_rect()
DayFontR.center=(985,20)
#Hour
HourFont = Font.render("Hour:"+str(Hour),1, Black)
HourFontR=HourFont.get_rect()
HourFontR.center=(1085,20)
#Minute
MinuteFont = Font.render("Minute:"+str(Minute),1, Black)
MinuteFontR=MinuteFont.get_rect()
MinuteFontR.center=(1200,20)

Clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(White)

    #Timer
    while Time==0:
        time.sleep(1)
        Minute=Minute+1
        screen.blit(MinuteFont, MinuteFontR)
        if Minute == 60:
            Hour=Hour+1        
            screen.blit(HourFont, HourFontR)
        if Hour==12:
            Hour=0
            Day=Day+1
            screen.blit(DayFont, DayFontR)

    pygame.display.flip()

    Clock.tick(60)

pygame.quit()