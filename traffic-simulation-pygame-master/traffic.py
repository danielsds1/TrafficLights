import pygame
import sys
import math as mt
import numpy as np
import datetime
from pygame import *
from pygame.locals import *
from pygame.sprite import *

#initialize pygame
pygame.init()

BLACK=(0,0,0)
WHITE=(255,255,255)
YELLOW=(255,255,0)
BGCOLOR=(128,128,128)

STREET=120
STRIPE=6
WIDTH=int(1280/2)
HEIGHT=int(720*2/3)

OCPMAP=[[0 for col in range(WIDTH)] for row in range(HEIGHT)]

CAPTION = 'Traffic Simulation'
SPEED=0
STREET_POS=[(0,(HEIGHT-STREET)/2,WIDTH,STREET),
            ((WIDTH-STREET)/2,0,STREET,HEIGHT)]

SIGNAL_POS=[[WIDTH/2-STREET/2-20,HEIGHT/2+STREET/2+5],
            [WIDTH/2+STREET/2+20,HEIGHT/2-STREET/2-5],
            [WIDTH/2-STREET/2-5,HEIGHT/2-STREET/2-20],
            [WIDTH/2+STREET/2+5,HEIGHT/2+STREET/2+20]]

STOP_LANE=[(WIDTH/2+STREET*5/4,HEIGHT/2-STREET/2,STRIPE,STREET),
           (WIDTH/2-STREET*5/4,HEIGHT/2-STREET/2,STRIPE,STREET),
           (WIDTH/2-STREET/2,HEIGHT/2+STREET+30,STREET,STRIPE),
           (WIDTH/2-STREET/2,HEIGHT/2-STREET-30,STREET,STRIPE)]

DOUBLE_LANE=[(0,HEIGHT/2-2,WIDTH/2-STREET*5/4,STRIPE/3),
             (0,HEIGHT/2+2,WIDTH/2-STREET*5/4,STRIPE/3),
             (WIDTH/2+STREET*5/4,HEIGHT/2-2,WIDTH/2-STREET*3/4,STRIPE/3),
             (WIDTH/2+STREET*5/4,HEIGHT/2+2,WIDTH/2-STREET*3/4,STRIPE/3),
             (WIDTH/2-2,0,STRIPE/3,HEIGHT/2-STREET*5/4),
             (WIDTH/2+2,0,STRIPE/3,HEIGHT/2-STREET*5/4),
             (WIDTH/2-STRIPE/3,HEIGHT/2+STREET+STREET/4,STRIPE/3,HEIGHT/2-STREET*3/4),
             (WIDTH/2+STRIPE/3,HEIGHT/2+STREET+STREET/4,STRIPE/3,HEIGHT/2-STREET*3/4)]

DASHED_LANE=[(0,HEIGHT/2-STREET/4,STRIPE*2,STRIPE/3),
             (0,HEIGHT/2+STREET/4,STRIPE*2,STRIPE/3),
             (WIDTH/2+STREET*5/4,HEIGHT/2-STREET/4,STRIPE*2,STRIPE/3),
             (WIDTH/2+STREET*5/4,HEIGHT/2+STREET/4,STRIPE*2,STRIPE/3),
             (WIDTH/2-STREET/4,0,STRIPE/3,STRIPE*2),
             (WIDTH/2+STREET/4,0,STRIPE/3,STRIPE*2),
             (WIDTH/2-STREET/4,HEIGHT/2+STREET*5/4,STRIPE/3,STRIPE*2),
             (WIDTH/2+STREET/4,HEIGHT/2+STREET*5/4,STRIPE/3,STRIPE*2)]

CROSSWALK=[(WIDTH/2-STREET,(HEIGHT-STREET)/2,STREET/2,STRIPE),
           ((WIDTH+STREET)/2,(HEIGHT-STREET)/2,STREET/2,STRIPE),
           ((WIDTH-STREET)/2,HEIGHT/2-STREET,STRIPE,STREET/2),
           ((WIDTH-STREET)/2,(HEIGHT+STREET)/2,STRIPE,STREET/2)]

COUNT_POS=[(SIGNAL_POS[0][0]-10,SIGNAL_POS[0][1]+5,20,20),
           (SIGNAL_POS[1][0]-10,SIGNAL_POS[1][1]-25,20,20),
           (SIGNAL_POS[2][0]-25,SIGNAL_POS[2][1]-10,20,20),
           (SIGNAL_POS[3][0]+5,SIGNAL_POS[3][1]-10,20,20)
        ]

CAR=[40,20]
MAX_SPEED=30
BTN_POS=[[20,20],[61,20],[102,20]]
velocity=[10,10]

#make a class of cars
class Cars(Sprite):
    
    def __init__(self,x,y,d):
        self.speed=5
        Sprite.__init__(self)
        self.image=image.load('img/'+d+'car.png')
        self.x=int(x) #variable denoting x position of car
        self.y=int(y) # y position of car
        self.rect=self.image.get_rect(center = (x,y)) #used to place the car
    
    #car1.move(xp,signal_counter,car2)
    def move(self,xp,sgn,a):
        
        xp=self.x+xp #new place for the car
        
        if xp>1200:
            xp = xp - 1200
        dista=xp-a.x
        
        if sgn == 0 or sgn == 1:
            self.rect.left=xp #move the car
            self.x=xp #update the car position
        elif sgn == 2:
            if self.x>WIDTH/2-STREET*5/4:
                self.rect.left=xp
                self.x=xp
            elif self.x>=WIDTH/2-STREET*5/4 and self.x<=550:
                pass
            elif dista>-20 and dista<20: #to check nearby cars
                pass
            else :
                self.rect.left=xp
                self.x=xp

class Signal(Sprite):
    def __init__(self,x,y,direction):
        Sprite.__init__(self)
        self.direction=direction
        self.image=image.load('img/'+direction+'red.png')
        self.rect=self.image.get_rect(center=(x,y))

    def change_sign(self,color):
            self.image=image.load('img/'+self.direction+color+'.png')
            '''if color=='red':
                if direction=='l':
                    for i in street/2:
                        OCPMAP[][]= 1'''
                    
class Watch(Sprite):
    def __init__(self,x,y):
        Sprite.__init__(self)
        self.image=image.load('img/off.png')
        self.rect=self.image.get_rect(center=(x,y))
    def change_num(self,num):
        self.image=image.load('img/'+str(num)+'.png')


class Button(Sprite):
    def __init__(self,button,x,y):
        Sprite.__init__(self)
        self.image=image.load('img/btn/'+button+'.png')
        self.rect=self.image.get_rect(center=(x,y))
    def hover(self,button):
        self.image=image.load('img/btn/'+button+'.png')

        
def drawBackground(frame,HEIGHT,WIDTH,STREET,STRIPE):
    frame.fill(BGCOLOR)
        
    #pygame.draw.rect(screen, color, (x,y,width,height), thickness)
    
    #Desenho das ruas
    pygame.draw.rect(frame,BLACK,STREET_POS[0],0) 
    pygame.draw.rect(frame,BLACK,STREET_POS[1],0)
    
    #Desenho das faixas dupla contínuas na rua horizontal 
    pygame.draw.rect(frame,YELLOW, DOUBLE_LANE[0],0) #desenho da faixa contínua
    pygame.draw.rect(frame,YELLOW, DOUBLE_LANE[1],0) #desenho da faixa contínua
    pygame.draw.rect(frame,YELLOW, DOUBLE_LANE[2],0)
    pygame.draw.rect(frame,YELLOW, DOUBLE_LANE[3],0)
    #Desenho das faixas dupla contínuas na rua vertical
    pygame.draw.rect(frame,YELLOW, DOUBLE_LANE[4],0)
    pygame.draw.rect(frame,YELLOW, DOUBLE_LANE[5],0)
    pygame.draw.rect(frame,YELLOW, DOUBLE_LANE[6],0)
    pygame.draw.rect(frame,YELLOW, DOUBLE_LANE[7],0)
    
    #Desenho das faixas de retenção na rua horizontal
    pygame.draw.rect(frame,WHITE, STOP_LANE[0],0)
    pygame.draw.rect(frame,WHITE, STOP_LANE[1],0)
    #Desenho das faixas de retenção na rua horizontal
    pygame.draw.rect(frame,WHITE, STOP_LANE[2],0)
    pygame.draw.rect(frame,WHITE, STOP_LANE[3],0)
    
    #Desenho das faixas tracejadas
    for i in range(int((WIDTH/2-STREET)//(STRIPE*4))-1):
        pygame.draw.rect(frame,WHITE, tuple(map(sum, zip(DASHED_LANE[0], (i*4*STRIPE,0,0,0)))),0)
        pygame.draw.rect(frame,WHITE, tuple(map(sum, zip(DASHED_LANE[1], (i*4*STRIPE,0,0,0)))),0)
        pygame.draw.rect(frame,WHITE, tuple(map(sum, zip(DASHED_LANE[2], (i*4*STRIPE,0,0,0)))),0)
        pygame.draw.rect(frame,WHITE, tuple(map(sum, zip(DASHED_LANE[3], (i*4*STRIPE,0,0,0)))),0)
    
    for i in range(int((HEIGHT/2-STREET)//(STRIPE*4))-1):
        
        pygame.draw.rect(frame,WHITE, tuple(map(sum, zip(DASHED_LANE[4], (0,i*4*STRIPE,0,0)))),0)
        pygame.draw.rect(frame,WHITE, tuple(map(sum, zip(DASHED_LANE[5], (0,i*4*STRIPE,0,0)))),0)
        
        pygame.draw.rect(frame,WHITE, tuple(map(sum, zip(DASHED_LANE[6], (0,i*4*STRIPE,0,0)))),0)
        pygame.draw.rect(frame,WHITE, tuple(map(sum, zip(DASHED_LANE[7], (0,i*4*STRIPE,0,0)))),0)    
    
    #Desenho das faixas de pedestres         
    for i in range(10):
        pygame.draw.rect(frame,WHITE, tuple(map(sum, zip(CROSSWALK[0], (0,i*STREET/10,0,0)))),0)
        pygame.draw.rect(frame,WHITE, tuple(map(sum, zip(CROSSWALK[1], (0,i*STREET/10,0,0)))),0) 
        
        pygame.draw.rect(frame,WHITE, tuple(map(sum, zip(CROSSWALK[2], (i*STREET/10,0,0,0)))),0)            
        pygame.draw.rect(frame,WHITE, tuple(map(sum, zip(CROSSWALK[3], (i*STREET/10,0,0,0)))),0)
    
    #Desenho do background do contador

    pygame.draw.rect(frame,BLACK, COUNT_POS[0],0)
    pygame.draw.rect(frame,BLACK, COUNT_POS[1],0)
    pygame.draw.rect(frame,BLACK, COUNT_POS[2],0)
    pygame.draw.rect(frame,BLACK, COUNT_POS[3],0)

def traffic():
    
    clock = pygame.time.Clock() # load clock
    #datetime.date.timetuple(datetime.datetime.now())
    #time.struct_time(tm_year=2018, tm_mon=7, tm_mday=4, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=2, tm_yday=185, tm_isdst=-1)
    start=datetime.date.timetuple(datetime.datetime.now())
    
    
    frame = pygame.display.set_mode((WIDTH, HEIGHT))
    display.set_caption(CAPTION)
    
    lrwatch=Watch(SIGNAL_POS[0][0]-5,SIGNAL_POS[0][1]+15)
    luwatch=Watch(SIGNAL_POS[0][0]+5,SIGNAL_POS[0][1]+15)

    rwatch1=Watch(SIGNAL_POS[1][0]-5,SIGNAL_POS[1][1]-15)
    ruwatch=Watch(SIGNAL_POS[1][0]+5,SIGNAL_POS[1][1]-15)

    uwatch1=Watch(SIGNAL_POS[2][0]-20,SIGNAL_POS[2][1])
    uwatch2=Watch(SIGNAL_POS[2][0]-10,SIGNAL_POS[2][1])

    dwatch1=Watch(SIGNAL_POS[3][0]+10,SIGNAL_POS[3][1])
    dwatch2=Watch(SIGNAL_POS[3][0]+20,SIGNAL_POS[3][1])

    xp=10
    
    car1=Cars(xp+0,HEIGHT/2+5*STRIPE/2,'l')
    car2=Cars(xp+50,HEIGHT/2+15*STRIPE/2,'l')
    car3=Cars(xp+100,HEIGHT/2+5*STRIPE/2,'l')
    car4=Cars(xp+150,HEIGHT/2+15*STRIPE/2,'l')
    
    lsignal=Signal(SIGNAL_POS[0][0],SIGNAL_POS[0][1],'l')
    lsignal.change_sign('green')
    rsignal=Signal(SIGNAL_POS[1][0],SIGNAL_POS[1][1],'r')
    rsignal.change_sign('green')
    usignal=Signal(SIGNAL_POS[2][0],SIGNAL_POS[2][1],'u')
    dsignal=Signal(SIGNAL_POS[3][0],SIGNAL_POS[3][1],'d')
    
    button0=Button('stop',BTN_POS[0][0],BTN_POS[0][1])
    button1=Button('pause',BTN_POS[1][0],BTN_POS[1][1])
    button2=Button('play',BTN_POS[2][0],BTN_POS[2][1])
    
    all_cars=Group(car1,car2,car3,car4)
    all_signals=Group(lsignal,rsignal,usignal,dsignal)
    all_watches=Group(lrwatch,luwatch,rwatch1,ruwatch,uwatch1,uwatch2,dwatch1,dwatch2)
    all_buttons=Group(button0,button1,button2)

    signal_counter=0
    cont=0
    green_time=10
    yellow_time=3
    red_time=10
    total_time=green_time+red_time+yellow_time

    while True:
        
        now=datetime.datetime.timetuple(datetime.datetime.now())
        seconds=(now.tm_hour*3600 + now.tm_min*60 + now.tm_sec)-(start.tm_hour*3600 + start.tm_min*60 + start.tm_sec)
        rtime=seconds%total_time
        #flaggreen=0

        if rtime==0:
            signal_counter=0
            lsignal.change_sign('green')
            rsignal.change_sign('green')
            usignal.change_sign('red')
            dsignal.change_sign('red')
        elif rtime==green_time:
            signal_counter=1
            lsignal.change_sign('yellow')
            rsignal.change_sign('yellow')
        elif rtime==green_time+yellow_time:
            signal_counter=2
            lsignal.change_sign('red')
            rsignal.change_sign('red')
            usignal.change_sign('green')
            dsignal.change_sign('green')
        elif rtime==green_time+red_time:
            signal_counter=2
            usignal.change_sign('yellow')
            dsignal.change_sign('yellow')

        if rtime<green_time:
            if cont!=rtime:
                lrwatch.change_num(mt.floor((green_time-rtime)/10))
                luwatch.change_num(mt.floor((green_time-rtime)%10))
                rwatch1.change_num(mt.floor((green_time-rtime)/10))
                ruwatch.change_num(mt.floor((green_time-rtime)%10))
                uwatch1.change_num('off')
                uwatch2.change_num('off')
                dwatch1.change_num('off')
                dwatch2.change_num('off')
            else:
                cont=rtime

        elif rtime<green_time+yellow_time:

            if cont!=rtime:
                lrwatch.change_num('off')
                luwatch.change_num('off')
                rwatch1.change_num('off')
                ruwatch.change_num('off')
            else:
                cont=rtime
        elif rtime<green_time+red_time:
            if cont!=rtime:
                
                lrwatch.change_num('off')
                luwatch.change_num('off')
                rwatch1.change_num('off')
                ruwatch.change_num('off')
                uwatch1.change_num(mt.floor((green_time+red_time-rtime)/10))
                uwatch2.change_num(mt.floor((green_time+red_time-rtime)%10))
                dwatch1.change_num(mt.floor((green_time+red_time-rtime)/10))
                dwatch2.change_num(mt.floor((green_time+red_time-rtime)%10))
            else:
                cont=rtime
        else:
            uwatch1.change_num('off')
            uwatch2.change_num('off')
            dwatch1.change_num('off')
            dwatch2.change_num('off')
        mouse_pos=mouse.get_pos()
        click=mouse.get_pressed()

        xp = 10
        
        drawBackground(frame,HEIGHT,WIDTH,STREET,STRIPE)
        #print(frame.get_at((int(WIDTH/2),int(HEIGHT/2))))
        car1.move(xp,signal_counter,car2)
        car2.move(xp,signal_counter,car3)
        car3.move(xp,signal_counter,car4)
        car4.move(xp,signal_counter,car1)
        
        
        e=event.pump()#Don't ever remove this for Odin's sake!
        
        #Stop execution
        if BTN_POS[0][0]+18>mouse_pos[0]>BTN_POS[0][0]-18 and BTN_POS[0][1]+18>mouse_pos[1]>BTN_POS[0][1]-18:
            button0.hover('stoph')
            if click[0]==1:
                break
        else:
            button0.hover('stop')
        #Pause execution
        if BTN_POS[1][0]+18>mouse_pos[0]>BTN_POS[1][0]-18 and BTN_POS[1][1]+18>mouse_pos[1]>BTN_POS[1][1]-18:
            button1.hover('pauseh')
            if click[0]==1:
                while True:
                    mouse_pos=mouse.get_pos()
                    click=mouse.get_pressed()
                    
                    e=event.pump() #Don't ever remove this for Odin's sake!
                    if BTN_POS[0][0]+18>mouse_pos[0]>BTN_POS[0][0]-18 and BTN_POS[0][1]+18>mouse_pos[1]>BTN_POS[0][1]-18:
                        button0.hover('stoph')
                        if click[0]==1:
                            pygame.quit()
                            quit()
                    else:
                        button0.hover('stop')
                    if BTN_POS[2][0]+18>mouse_pos[0]>BTN_POS[2][0]-18 and BTN_POS[2][1]+18>mouse_pos[1]>BTN_POS[2][1]-18:
                        button2.hover('playh')
                        if click[0]==1:
                            button2.hover('play')
                            start=datetime.date.timetuple(datetime.datetime.now())
                            break
                    else:
                        button2.hover('play')
                    
                    drawBackground(frame,HEIGHT,WIDTH,STREET,STRIPE)    
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
    clock = pygame.time.Clock() # load clock



if __name__ =='__main__':
    traffic()
