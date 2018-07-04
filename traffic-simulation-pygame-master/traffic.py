import pygame
import sys
import math
from pygame import *
from pygame.locals import *
from pygame.sprite import *



#initialize pygame
pygame.init()


STREET=120
STRIPE=6
WIDTH=1280
HEIGHT=720
CAPTION = 'Traffic Simulation'
SPEED=0
SIGNAL_POS=[[WIDTH/2-STREET/2-20,HEIGHT/2+STREET/2+5],
[WIDTH/2+STREET/2+20,HEIGHT/2-STREET/2-5],
[WIDTH/2-STREET/2-5,HEIGHT/2-STREET/2-20],
[WIDTH/2+STREET/2+5,HEIGHT/2+STREET/2+20]]
MAX_SPEED=30
BTN_POS=[[20,20],[61,20],[102,20]]
velocity=[10,10]

#make a class of cars
class Cars(Sprite):
    def __init__(self,x,y):
        Sprite.__init__(self)
        self.image=image.load('img/lcar.png')
        self.x=int(x) #variable denoting x position of car
        self.y=int(y) # y position of car
        self.rect=self.image.get_rect(center = (x,y)) #used to place the car

    def move(self,xp,sgn,a):
        
        xp=self.x+xp #new place for the car
        
        if xp>1200:
            xp = xp - 1200
        dista=xp-a.x
       
        if sgn == 0 or sgn == 1:
            self.rect.left=xp #move the car
            self.x=xp #update the car position
        elif sgn == 2:
            if self.x>500:
                self.rect.left=xp
                self.x=xp
            elif self.x>=500 and self.x<=550:
                pass
            elif dista>-20 and dista<20: #to check nearby cars
                pass
            else :
                self.rect.left=xp
                self.x=xp

class Signal(Sprite):
    def __init__(self,x,y,direction):
        Sprite.__init__(self)
        if direction=='l':
            self.image=image.load('img/lgreen.png')
        elif direction=='r':
            self.image=image.load('img/rgreen.png')
        elif direction=='u':
            self.image=image.load('img/ured.png')
        elif direction=='d':
            self.image=image.load('img/dred.png')
        self.rect=self.image.get_rect(center=(x,y))
    def change_sign(self,color):
            self.image=image.load(color)

class Watch(Sprite):
    def __init__(self,x,y):
        Sprite.__init__(self)
        self.image=image.load('img/9.png')
        self.rect=self.image.get_rect(center=(x,y))

class Button(Sprite):
    def __init__(self,button,x,y):
        Sprite.__init__(self)
        self.image=image.load('img/btn/'+button+'.png')
        self.rect=self.image.get_rect(center=(x,y))
    def hover(self,button):
        self.image=image.load('img/btn/'+button+'.png')

        
def drawBackground(frame,HEIGHT,WIDTH,STREET,STRIPE):
    frame.fill((128,128,128))
        
    #pygame.draw.rect(screen, color, (x,y,width,height), thickness)
    
    #Desenho das ruas
    pygame.draw.rect(frame,(0,0,0), (0,(HEIGHT-STREET)/2,WIDTH,STREET),0) 
    pygame.draw.rect(frame,(0,0,0), ((WIDTH-STREET)/2,0,STREET,HEIGHT),0)
    
    #Desenho das faixas dupla contínuas na rua horizontal 
    pygame.draw.rect(frame,(255,255,0), (0,HEIGHT/2-2,WIDTH/2-STREET*5/4,STRIPE/3),0) #desenho da faixa contínua
    pygame.draw.rect(frame,(255,255,0), (0,HEIGHT/2+2,WIDTH/2-STREET*5/4,STRIPE/3),0) #desenho da faixa contínua
    pygame.draw.rect(frame,(255,255,0), (WIDTH/2+STREET*5/4,HEIGHT/2-2,WIDTH/2-STREET*3/4,STRIPE/3),0)
    pygame.draw.rect(frame,(255,255,0), (WIDTH/2+STREET*5/4,HEIGHT/2+2,WIDTH/2-STREET*3/4,STRIPE/3),0)
    
    #Desenho das faixas de retenção na rua horizontal
    pygame.draw.rect(frame,(255,255,255), (WIDTH/2+STREET*5/4,HEIGHT/2-STREET/2,STRIPE,STREET),0)
    pygame.draw.rect(frame,(255,255,255), (WIDTH/2-STREET*5/4,HEIGHT/2-STREET/2,STRIPE,STREET),0)
    
    #Desenho das faixas dupla contínuas na rua vertical
    pygame.draw.rect(frame,(255,255,0), (WIDTH/2-2,0,STRIPE/3,HEIGHT/2-STREET*5/4),0)
    pygame.draw.rect(frame,(255,255,0), (WIDTH/2+2,0,STRIPE/3,HEIGHT/2-STREET*5/4),0)
    pygame.draw.rect(frame,(255,255,0), (WIDTH/2-STRIPE/3,HEIGHT/2+STREET+STREET/4,STRIPE/3,HEIGHT/2-STREET*3/4),0)
    pygame.draw.rect(frame,(255,255,0), (WIDTH/2+STRIPE/3,HEIGHT/2+STREET+STREET/4,STRIPE/3,HEIGHT/2-STREET*3/4),0)
    
    #Desenho das faixas de retenção na rua horizontal
    pygame.draw.rect(frame,(255,255,255), (WIDTH/2-STREET/2,HEIGHT/2+STREET+30,STREET,STRIPE),0)
    pygame.draw.rect(frame,(255,255,255), (WIDTH/2-STREET/2,HEIGHT/2-STREET-30,STREET,STRIPE),0)
    
    #Desenho das faixas tracejadas
    for i in range(int((WIDTH/2-STREET)//(STRIPE*4))-1):
        pygame.draw.rect(frame,(255,255,255), (i*4*STRIPE,HEIGHT/2-STREET/4,STRIPE*2,STRIPE/3),0)
        pygame.draw.rect(frame,(255,255,255), (i*4*STRIPE,HEIGHT/2+STREET/4,STRIPE*2,STRIPE/3),0)
        
        pygame.draw.rect(frame,(255,255,255), (i*4*STRIPE+WIDTH/2+STREET*5/4,HEIGHT/2-STREET/4,STRIPE*2,STRIPE/3),0)
        pygame.draw.rect(frame,(255,255,255), (i*4*STRIPE+WIDTH/2+STREET*5/4,HEIGHT/2+STREET/4,STRIPE*2,STRIPE/3),0)
    
    for i in range(int((HEIGHT/2-STREET)//(STRIPE*4))-1):
        pygame.draw.rect(frame,(255,255,255), (WIDTH/2-STREET/4,i*4*STRIPE,STRIPE/3,STRIPE*2),0)
        pygame.draw.rect(frame,(255,255,255), (WIDTH/2+STREET/4,i*4*STRIPE,STRIPE/3,STRIPE*2),0)
        
        pygame.draw.rect(frame,(255,255,255), (WIDTH/2-STREET/4,i*4*STRIPE+HEIGHT/2+STREET*5/4,STRIPE/3,STRIPE*2),0)
        pygame.draw.rect(frame,(255,255,255), (WIDTH/2+STREET/4,i*4*STRIPE+HEIGHT/2+STREET*5/4,STRIPE/3,STRIPE*2),0)    
    
    #Desenho das faixas de pedestres         
    for i in range(10):
        pygame.draw.rect(frame,(255,255,255), (WIDTH/2-STREET,(HEIGHT-STREET)/2+i*STREET/10,STREET/2,STRIPE),0)
        pygame.draw.rect(frame,(255,255,255), ((WIDTH+STREET)/2,(HEIGHT-STREET)/2+i*STREET/10,STREET/2,STRIPE),0)
        
        pygame.draw.rect(frame,(255,255,255), ((WIDTH-STREET)/2+i*STREET/10,HEIGHT/2-STREET,STRIPE,STREET/2),0)            
        pygame.draw.rect(frame,(255,255,255), ((WIDTH-STREET)/2+i*STREET/10,(HEIGHT+STREET)/2,STRIPE,STREET/2),0)
    #Desenho do background do contador

    pygame.draw.rect(frame,(0,0,0), (SIGNAL_POS[0][0]-10,SIGNAL_POS[0][1]+5,20,20),0)
    pygame.draw.rect(frame,(0,0,0), (SIGNAL_POS[1][0]-10,SIGNAL_POS[1][1]-25,20,20),0)
    pygame.draw.rect(frame,(0,0,0), (SIGNAL_POS[2][0]-25,SIGNAL_POS[2][1]-10,20,20),0)
    pygame.draw.rect(frame,(0,0,0), (SIGNAL_POS[3][0]+5,SIGNAL_POS[3][1]-10,20,20),0)
'''
def button(button0,btnum,):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    
    pass
'''
def traffic():

    clock = pygame.time.Clock() # load clock
    frame = pygame.display.set_mode((WIDTH, HEIGHT))
    display.set_caption(CAPTION)
    watch01=Watch(SIGNAL_POS[0][0]-5,SIGNAL_POS[0][1]+15)
    watch02=Watch(SIGNAL_POS[0][0]+5,SIGNAL_POS[0][1]+15)

    watch11=Watch(SIGNAL_POS[1][0]+5,SIGNAL_POS[1][1]-15)
    watch12=Watch(SIGNAL_POS[1][0]-5,SIGNAL_POS[1][1]-15)

    watch21=Watch(SIGNAL_POS[2][0]-10,SIGNAL_POS[2][1])
    watch22=Watch(SIGNAL_POS[2][0]-20,SIGNAL_POS[2][1])

    watch31=Watch(SIGNAL_POS[3][0]+10,SIGNAL_POS[3][1])
    watch32=Watch(SIGNAL_POS[3][0]+20,SIGNAL_POS[3][1])

    xp=10; 
    car1=Cars(xp+0,HEIGHT/2+5*STRIPE/2)
    car2=Cars(xp+50,HEIGHT/2+15*STRIPE/2)
    car3=Cars(xp+100,HEIGHT/2+5*STRIPE/2)
    car4=Cars(xp+150,HEIGHT/2+15*STRIPE/2)
    
    signal0=Signal(SIGNAL_POS[0][0],SIGNAL_POS[0][1],'l')
    signal1=Signal(SIGNAL_POS[1][0],SIGNAL_POS[1][1],'r')
    signal2=Signal(SIGNAL_POS[2][0],SIGNAL_POS[2][1],'u')
    signal3=Signal(SIGNAL_POS[3][0],SIGNAL_POS[3][1],'d')
    
    button0=Button('stop',BTN_POS[0][0],BTN_POS[0][1])
    button1=Button('pause',BTN_POS[1][0],BTN_POS[1][1])
    button2=Button('play',BTN_POS[2][0],BTN_POS[2][1])
    
    all_cars=Group(car1,car2,car3,car4)
    all_signals=Group(signal0,signal1,signal2,signal3)
    all_watches=Group(watch01,watch02,watch11,watch12,watch21,watch22,watch31,watch32)
    all_buttons=Group(button0,button1,button2)
    signal_list=[['img/lgreen.png','img/lyellow.png','img/lred.png'],
    ['img/rgreen.png','img/ryellow.png','img/rred.png'],
    ['img/ugreen.png','img/uyellow.png','img/ured.png'],
    ['img/dgreen.png','img/dyellow.png','img/dred.png']]

    signal_counter=0
    cont=0
       
    while True:
        
        mouse_pos=mouse.get_pos()
        click=mouse.get_pressed()
        #print(click[0])
        xp = 10
        
        drawBackground(frame,HEIGHT,WIDTH,STREET,STRIPE)

        car1.move(xp,signal_counter,car2)
        car2.move(xp,signal_counter,car3)
        car3.move(xp,signal_counter,car4)
        car4.move(xp,signal_counter,car1)
        
        
        e=event.pump()
        if click[2]==1:
            break
        if click[0]==1:
            signal_counter+=1
            if signal_counter>2:
                signal_counter=0 
            signal0.change_sign(signal_list[0][signal_counter])
            signal1.change_sign(signal_list[1][signal_counter])
            signal2.change_sign(signal_list[2][2-signal_counter])
            signal3.change_sign(signal_list[3][2-signal_counter])

        if BTN_POS[0][0]+18>mouse_pos[0]>BTN_POS[0][0]-18 and BTN_POS[0][1]+18>mouse_pos[1]>BTN_POS[0][1]-18:
            button0.hover('stoph')
            if click[0]==1:
                break
        else:
            button0.hover('stop')
        
        if BTN_POS[1][0]+18>mouse_pos[0]>BTN_POS[1][0]-18 and BTN_POS[1][1]+18>mouse_pos[1]>BTN_POS[1][1]-18:
            button1.hover('pauseh')
            if click[0]==1:
                while True:
                    mouse_pos=mouse.get_pos()
                    click=mouse.get_pressed()
                    e=event.pump()

                    if BTN_POS[2][0]+18>mouse_pos[0]>BTN_POS[2][0]-18 and BTN_POS[2][1]+18>mouse_pos[1]>BTN_POS[2][1]-18:
                        button2.hover('playh')
                        if click[0]==1:
                            button2.hover('play')
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
