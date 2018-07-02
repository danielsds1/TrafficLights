import pygame
import sys
import math
from pygame import *
from pygame.locals import *
from pygame.sprite import *





#initialize pygame
pygame.init()


street=120
stripe=6
WIDTH=960
HEIGHT=720
CAPTION = 'Traffic Simulation'
SPEED=0

MAX_SPEED=30
velocity=[10,10]


#make a class of cars
class Cars(Sprite):
    def __init__(self,x,y):
        Sprite.__init__(self)
        self.image=image.load('img/carl.png')
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
            elif dista>-200 and dista<200: #to check nearby cars
                pass
            else :
                self.rect.left=xp
                self.x=xp


class Signal(Sprite):
    def __init__(self,x,y):
        Sprite.__init__(self)
        self.image=image.load('img/green.png')
        self.rect=self.image.get_rect(center=(x,y))
    def change_sign(self,color):
            self.image=image.load(color)

class Watch(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image=image.load('img/9.png')
        self.rect=self.image.get_rect(center=(732,50))
        self.image=image.load('img/9.png')
        self.rect=self.image.get_rect(center=(774,50))
    pass



def traffic():

    clock = pygame.time.Clock() # load clock

    
    frame = pygame.display.set_mode((WIDTH, HEIGHT))
    display.set_caption(CAPTION)
    watch=Watch()
    xp=100; 
    car1=Cars(xp+0,HEIGHT/2+2*stripe)
    car2=Cars(xp+50,HEIGHT/2+5*stripe)
    car3=Cars(xp+100,HEIGHT/2+8*stripe)
    car4=Cars(xp+150,HEIGHT/2+2*stripe)
    
    signal1=Signal((WIDTH-street)/2,(HEIGHT-street)/2)
    
    all_cars=Group(car1,car2,car3,car4)
    all_signals=Group(signal1)
    all_watches=Group(watch)
    
    
    signal_list=['img/green.png','img/yellow.png','img/red.png'];

    signal_counter=0;
    
    
    
    while True:
        
        xp = 2
        car1.move(xp,signal_counter,car2)
        car2.move(xp,signal_counter,car3)
        car3.move(xp,signal_counter,car4)
        car4.move(xp,signal_counter,car1)
        e=event.wait()
        if e.type==KEYDOWN:
          if e.key==K_ESCAPE:
              break
        if e.type==MOUSEBUTTONDOWN:
            signal_counter+=1
            if signal_counter>2:
                signal_counter=0 
            signal1.change_sign(signal_list[signal_counter])
        
        
        frame.fill((0,128,0))
        
        #pygame.draw.rect(screen, color, (x,y,width,height), thickness)
        
        #Desenho das ruas
        pygame.draw.rect(frame,(0,0,0), (0,(HEIGHT-street)/2,WIDTH,street),0) 
        pygame.draw.rect(frame,(0,0,0), ((WIDTH-street)/2,0,street,HEIGHT),0)
        
        #Desenho das faixas dupla contínuas na rua horizontal 
        pygame.draw.rect(frame,(255,255,0), (0,HEIGHT/2-2,WIDTH/2-street*5/4,stripe/3),0) #desenho da faixa contínua
        pygame.draw.rect(frame,(255,255,0), (0,HEIGHT/2+2,WIDTH/2-street*5/4,stripe/3),0) #desenho da faixa contínua
        pygame.draw.rect(frame,(255,255,0), (WIDTH/2+street*5/4,HEIGHT/2-2,WIDTH/2-street*3/4,stripe/3),0)
        pygame.draw.rect(frame,(255,255,0), (WIDTH/2+street*5/4,HEIGHT/2+2,WIDTH/2-street*3/4,stripe/3),0)
        
        #Desenho das faixas de retenção na rua horizontal
        pygame.draw.rect(frame,(255,255,255), (WIDTH/2+street*5/4,HEIGHT/2-street/2,stripe,street),0)
        pygame.draw.rect(frame,(255,255,255), (WIDTH/2-street*5/4,HEIGHT/2-street/2,stripe,street),0)
        
        #Desenho das faixas dupla contínuas na rua vertical
        pygame.draw.rect(frame,(255,255,0), (WIDTH/2-2,0,stripe/3,HEIGHT/2-street*5/4),0)
        pygame.draw.rect(frame,(255,255,0), (WIDTH/2+2,0,stripe/3,HEIGHT/2-street*5/4),0)
        pygame.draw.rect(frame,(255,255,0), (WIDTH/2-stripe/3,HEIGHT/2+street+street/4,stripe/3,HEIGHT/2-street*3/4),0)
        pygame.draw.rect(frame,(255,255,0), (WIDTH/2+stripe/3,HEIGHT/2+street+street/4,stripe/3,HEIGHT/2-street*3/4),0)
        
        
        #Desenho das faixas de retenção na rua horizontal
        pygame.draw.rect(frame,(255,255,255), (WIDTH/2-street/2,HEIGHT/2+street+30,street,stripe),0)
        pygame.draw.rect(frame,(255,255,255), (WIDTH/2-street/2,HEIGHT/2-street-30,street,stripe),0)
        
        #Desenho das faixas tracejadas
        for i in range(int((WIDTH/2-street)//(stripe*4))-1):
            pygame.draw.rect(frame,(255,255,255), (i*4*stripe,HEIGHT/2-street/4,stripe*2,stripe/3),0)
            pygame.draw.rect(frame,(255,255,255), (i*4*stripe,HEIGHT/2+street/4,stripe*2,stripe/3),0)
            
            pygame.draw.rect(frame,(255,255,255), (i*4*stripe+WIDTH/2+street*5/4,HEIGHT/2-street/4,stripe*2,stripe/3),0)
            pygame.draw.rect(frame,(255,255,255), (i*4*stripe+WIDTH/2+street*5/4,HEIGHT/2+street/4,stripe*2,stripe/3),0)
            
        #Desenho das faixas de pedestres         
        for i in range(10):
            pygame.draw.rect(frame,(255,255,255), (WIDTH/2-street,(HEIGHT-street)/2+i*street/10,street/2,stripe),0)
            pygame.draw.rect(frame,(255,255,255), ((WIDTH+street)/2,(HEIGHT-street)/2+i*street/10,street/2,stripe),0)
            
            pygame.draw.rect(frame,(255,255,255), ((WIDTH-street)/2+i*street/10,HEIGHT/2-street,stripe,street/2),0)            
            pygame.draw.rect(frame,(255,255,255), ((WIDTH-street)/2+i*street/10,(HEIGHT+street)/2,stripe,street/2),0)
            
            
        #pygame.draw.rect(frame,(0,0,0), (0,235,WIDTH,60),0)
        
        #pygame.draw.rect(frame,(0,0,0), (350,0,60,HEIGHT),0)
        all_cars.draw(frame)
        all_signals.draw(frame)
        all_watches.draw(frame)
        display.update()
        pygame.display.flip()
    pygame.quit()

    clock = pygame.time.Clock() # load clock





if __name__ =='__main__':
    traffic()
