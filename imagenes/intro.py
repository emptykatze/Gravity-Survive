import pygame,time,sys
from pygame.locals import *


(ancho, alto) = (1280, 720)
screen = pygame.display.set_mode((ancho,alto))


tamañoplaneta=43

sol= pygame.image.load("imagenes/intro/sol.png").convert_alpha()
sol=pygame.transform.scale(sol,(tamañoplaneta*10,tamañoplaneta*10))

    
planeta1 = pygame.image.load("imagenes/intro/p5.png").convert_alpha()
planeta1=pygame.transform.scale(planeta1,(int(tamañoplaneta/2+2),int(tamañoplaneta/2)))

planeta2 = pygame.image.load("imagenes/intro/p7.png").convert_alpha()
planeta2=pygame.transform.scale(planeta2,(int(tamañoplaneta/2+12),int(tamañoplaneta/2+10)))

planeta3 = pygame.image.load("imagenes/intro/p9.png").convert_alpha()
planeta3=pygame.transform.scale(planeta3,(int(tamañoplaneta/2+22),int(tamañoplaneta/2+20)))

screen.blit(planeta1,(ancho/2-600,alto/2-50))
screen.blit(sol,(ancho/2-520,alto/2-250))

pygame.display.flip()


xp=ancho/2-500
yp=alto/2-25
vp=0.6


def intro(xp,yp,vp):
    
    xp=xp+vp
    absvp=vp/abs(vp)
       
    if vp>0:
        screen.blit(sol,(ancho/2-500,alto/2-250))
        vp=vp/1.0005
    screen.blit(planeta1,(xp,yp))
    if vp<0:
        screen.blit(sol,(ancho/2-500,alto/2-250))
        vp=vp*1.0005       
    pygame.display.flip()
            
    if xp>ancho-500 or xp<0+100:
        vp=-vp

        
   

