# -*- coding: utf-8 -*-
"""
Juego sistema planetario
"""
import pygame,sys,time,math
import numpy as np
from pygame.locals import*
from librerias import Colores as c
from imagenes import imagenes  as im
from sonidos import sonidos as s
from imagenes import intro 
from decimal import Decimal
import os

if os.path.exists("save.txt"):pass
else:
    file=open("save.txt","w")
    av=[]
    file.write("1")
    for i in range(60):
        file.write("0")
    file.close()
file=open("save.txt","r")
global avance
leer=file.read()
avance=[]
for x in range(60):
    avance=avance+[int(leer[x])]
file.close()


fond=int(1280)
fondo1=pygame.transform.scale(pygame.image.load("imagenes/fondos/m.png"),(1280,720))
#fondo1=pygame.image.load("imagenes/menu_principal/negro.png")
#fondo1=im.fondo2
#tamaño de pantalla
ancho,alto=1280,720
pantalla = pygame.display.set_mode((ancho, alto))#,pygame.FULLSCREEN)
#icono
pygame.display.set_icon(im.icono)
#CLASES Y DEFINICIONES DE FUNCIÓNES
class cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,0,0,1,1)
    def update(self):
        self.left,self.top=pygame.mouse.get_pos()
        
class boton(pygame.sprite.Sprite):
    def __init__(self,imagen1,imagen2,x=0,y=0):
        self.im_normal=imagen1
        self.im_seleccion=imagen2 
        self.im_actual=self.im_normal
        self.rect=self.im_actual.get_rect()
        self.rect.left,self.rect.top=(x,y)
    def update(self,pantalla,cursor):
        if cursor.colliderect(self.rect):
            self.im_actual=self.im_seleccion
        else:
            self.im_actual=self.im_normal
        pantalla.blit(self.im_actual,self.rect)


class slider(pygame.sprite.Sprite):
    def __init__(self,imagen1,imagen2,x=0,y=0,xs=0,ys=0,color=c.purple):
        self.im_fondo=imagen1
        self.im_slider=imagen2 
        self.im_actual=self.im_fondo
        self.rect=self.im_fondo.get_rect()
        self.rects=self.im_slider.get_rect()
        self.rect.left,self.rect.top=(x,y-10)
        self.rects.left,self.rects.top=(xs,ys)
        self.x=x
        self.y=y
        self.c=color
        self.xs=xs
    def update(self,pantalla,cursor):
        if cursor.colliderect(self.rect) and click_sostenido==True:
            global deslizador
            deslizador=1    
        else:
            deslizador=0
        if cursor.colliderect(self.rect) and click2==True:
            pygame.mixer.Sound.play(s.click)
            
        pantalla.blit(self.im_fondo,self.rect)
        pygame.draw.rect(pantalla, self.c, [self.x, self.y, self.rects.centerx-self.x, 20])
        pantalla.blit(self.im_slider,self.rects)
        
        
def texto(texto,tamaño=30,x=0,y=0,color=c.white,fuente=None):
    font=pygame.font.Font(fuente,tamaño)
    tex=font.render(texto,0,color)
    pantalla.blit(tex, (x,y))



""" explosiones """
animacion_explosion={'t1':[],'t2':[],'t3':[],'t4':[]}
for x in range(24):
    archivo_explosiones=f'expl_08_{x:04d}.png'
    imagenes=pygame.image.load(f'imagenes/explosiones/8/{archivo_explosiones}')
    
    imagenes_t1=pygame.transform.scale(imagenes,(32,32))
    animacion_explosion['t1'].append(imagenes_t1)
    
    imagenes_t2=pygame.transform.scale(imagenes,(64,64))
    animacion_explosion['t2'].append(imagenes_t2)
    
    imagenes_t3=pygame.transform.scale(imagenes,(128,128))
    animacion_explosion['t3'].append(imagenes_t3)
    
    imagenes_t4=pygame.transform.scale(imagenes,(256,256))
    animacion_explosion['t4'].append(imagenes_t4)
    
class explosiones(pygame.sprite.Sprite):
    def __init__(self,centro,dimensiones):
        pygame.sprite.Sprite.__init__(self)
        self.dimensiones=dimensiones
        self.image=animacion_explosion[self.dimensiones][0]
        self.rect=self.image.get_rect()
        self.rect.center=centro
        self.fotograma=0
        self.frecuencia_fotograma=30
        self.actualizacion=pygame.time.get_ticks()
    def update(self):
        ahora=pygame.time.get_ticks()
        if ahora-self.actualizacion>self.frecuencia_fotograma:
            self.actualizacion=ahora
            self.fotograma+=1
            if self.fotograma== len(animacion_explosion[self.dimensiones]):
                self.kill()
            else:
                centro=self.rect.center
                self.image=animacion_explosion[self.dimensiones][self.fotograma]
                self.rect=self.image.get_rect()
                self.rect.center=centro






#grupos de sprites
sprites=pygame.sprite.Group()
Explosiones=pygame.sprite.Group()

cursor=cursor()
reloj=pygame.time.Clock()

"""
Definir clase planeta ////////////////////////////////////////////////////////////////7
"""
t=0
class planeta(pygame.sprite.Sprite):
    def __init__(self, masa, posicion, velocidad,tamaño=20,imagen=intro.planeta1): #posicion y velocidad = vectores de R2
        super().__init__()        
        self.masa = masa
        self.momentum = masa * np.array(velocidad)
        self.imagen=imagen
        self.p=posicion
        self.rect=self.imagen.get_rect()
        self.pos=self.rect.centerx,self.rect.centery
        self.posicion = np.array(posicion) 
        self.tamaño=tamaño
 

    #Calcular fuerza sobre self por p2 (Ley de gravitacion universal)
    def fuerzag(self, p2):
        G =0.8 #valor real=0.000000000066738
        r_vec = self.posicion - p2.posicion
        r_mag = np.linalg.norm(r_vec)
        r_unit = r_vec / r_mag
        fuerza_mag = G * self.masa * p2.masa / r_mag ** 2
        fuerza_vec = -fuerza_mag * r_unit
        return fuerza_vec
    
    def im(self):
        im=pygame.transform.scale(self.imagen,(self.tamaño,self.tamaño))
        return im
    def distancia(p,COHETE):
        centro=p.posicion-(COHETE.tamaño/2,COHETE.tamaño/2)
        cohete=np.sqrt(((p.centro[0])-(COHETE.posicion[0]))**2+((p.centro[1])-(COHETE.posicion[1]))**2)
        return cohete

# escoger un elemento random de una lista
def rand(a):
        return np.random.choice(a)



# FUNCIÓN PRINCIPAL
def main():
    pygame.init()   
    pygame.mixer.init()
    pygame.display.set_caption('Juego')
    
    #SONIDOS
    vol=0
    sound=0.5
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.Sound.set_volume(s.click,sound)
    sclick=pygame.mixer.Sound.play(s.click)
      
    #Pantallas del juego
    menu=True
    juego=False
    pausa=False
    menu2=False
    mundo1=False
    mundo2=False
    mundo3=False
    lost=False
    siguiente_nivel=False
    siguiente2=False
    ganar=False
    como_jugar=False
    como_jugar2=False
    como_jugar3=False
    como_jugar4=False
    como_jugar5=False
    como_jugar6=False
    #Variables globales
    global click
    click=False
    global click2
    click2=False
    global click_sostenido
    click_sostenido=False
    global mousex,mousey 
    
    #Posiciones de los sliders
    volx=450
    posvolx=625
    possonx=625

    #pantalla de menu
    vel_fondo=2
    pos_fondo=0
       
    
    ##intro
    intro_old=None
    xp1=ancho/2-170
    yp1=alto/2-25+12
    vp1=8
    
    xp2=ancho/2-300
    yp2=alto/2-25+5
    vp2=6
    
    xp3=ancho/2-500
    yp3=alto/2-25
    vp3=4

    
    """ Parametros del Juego """

    #Parametros de tiempo
    global t
    t = 0
    """" << PLANETAS >> """
    pl1=im.p1
    pl2=im.p2
    pl3=im.p3
    pl4=im.p4
    pl5=im.p5
    pl6=im.p6
    pl7=im.p7
    pl=[pl1,pl2,pl3,pl4,pl5,pl6,pl7]
    m_pl=[50,100,200,300,400,500]
    
    """" << ESTRELLAS >> """
    e1=im.e1
    e2=im.e2
    e3=im.e3
    e4=im.e4
    e=[e1,e2,e3,e4]
    m_e=[[500000,e1],[1000000,e2],[1500000,e3]]
    
    combustible=1
    
    lv1,lv2,lv3,lv4,lv5,lv6,lv7,lv8,lv9,lv10,lv11,lv12,lv13,lv14,lv15,lv16,lv17,lv18,lv19,lv20=False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False
    lv21,lv22,lv23,lv24,lv25,lv26,lv27,lv28,lv29,lv30,lv31,lv32,lv33,lv34,lv35,lv36,lv37,lv38,lv39,lv40=False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False
    lv41,lv42,lv43,lv44,lv45,lv46,lv47,lv48,lv49,lv50,lv51,lv52,lv53,lv54,lv55,lv56,lv57,lv58,lv59,lv60=False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False
    
    nivelesm1=[lv1,lv2,lv3,lv4,lv5,lv6,lv7,lv8,lv9,lv10,lv11,lv12,lv13,lv14,lv15,lv16,lv17,lv18,lv19,lv20]
    nivelesm2=[lv21,lv22,lv23,lv24,lv25,lv26,lv27,lv28,lv29,lv30,lv31,lv32,lv33,lv34,lv35,lv36,lv37,lv38,lv39,lv40]
    nivelesm3=[lv41,lv42,lv43,lv44,lv45,lv46,lv47,lv48,lv49,lv50,lv51,lv52,lv53,lv54,lv55,lv56,lv57,lv58,lv59,lv60]
    #niveles del mundo 1
    n=0
    nm1=[]
    while n<20:
        n=n+1
        nm1=nm1+[False]
    #niveles del mundo 2
    n=0
    nm2=[]
    while n<20:
        n=n+1
        nm2=nm2+[False]
    #niveles del mundo 3
    n=0
    nm3=[]
    while n<21:
        n=n+1
        nm3=nm3+[False]
    #total de niveles
    nt=nm1+nm2+nm3
    # nivel en el que se esta actualmente
    n=0
    l=[]
    while n<60:
        n=n+1
        l=l+[False]
    
    # LOOP PRINCIPAL
    UP=0
    DOWN=0
    LEFT=0
    RIGHT=0
    
    """ #########################################################"""
    """ #########################################################"""
    """ ######################### WHILE #########################"""
    """ #########################################################"""    
    """ #########################################################"""
    

    while True:
        """ #########################################################"""
        """ #########################################################"""
        """ ######################## NIVELES ########################"""
        """ #########################################################"""    
        """ #########################################################"""
                
        """ #########################################################"""
        """ #########################################################"""
        """ ######################## MUNDO 1 ########################"""
        """ #########################################################"""    
        """ #########################################################"""
        if nm1[0]==True:
            dt=0.15
            combustible=500
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/2.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [200, 250], [0,15],50,im.p5)
            p2 = planeta(50, [100, 360], [0,10],50,im.p2)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]-(p1.tamaño)+17,p1.posicion[1]), [0,0],10,im.e4)
            planetas= [COHETE,p1,e1,p2]
            planetasv=[p1,p2]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[0]=False
            if True in l:        
                l[l.index(True)]=False
            l[0]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[1]==True:
            dt=0.15
            combustible=500
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/4.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [250, 100], [0,10],50,im.p3)
            p2 = planeta(50, [100, 360], [0,10],50,im.p4)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]-(p1.tamaño)+18,p1.posicion[1]), [0,0],10,im.e4)
            planetas= [COHETE,p1,e1,p2]
            planetasv=[p1,p2]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[1]=False
            if True in l:        
                l[l.index(True)]=False
            l[1]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[2]==True:
            dt=0.15
            combustible=200
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/6.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [600, 50], [-15,5],50,im.p5)
            p2 = planeta(50, [100, 360], [0,10],50,im.p6)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]-(p1.tamaño)+18,p1.posicion[1]), [0,0],10,im.e4)
            planetas= [COHETE,p1,e1,p2]
            planetasv=[p1,p2]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[2]=False
            if True in l:        
                l[l.index(True)]=False
            l[2]=True
            juego=True
            fondojuegox,fondojuegoy=0,0 
            fondo_nivel=im.fondo_mundo1
            
        if nm1[3]==True:
            dt=0.15
            combustible=150
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/8.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [900, 360], [0,-15],50,im.p7)
            p2 = planeta(50, [100, 360], [0,10],50,im.p8)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]-(p1.tamaño)+18,p1.posicion[1]), [0,0],10,im.e4)
            planetas= [COHETE,p1,e1,p2]
            planetasv=[p1,p2]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[3]=False
            if True in l:        
               l[l.index(True)]=False
            l[3]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[4]==True:
            dt=0.15
            combustible=150
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/9.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [600, 100], [15,0],50,im.p8)
            p2 = planeta(50, [600, 620], [-15,0],50,im.p9)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]-(p1.tamaño)+18,p1.posicion[1]), [0,0],10,im.e4)
            planetas= [COHETE,p1,e1,p2]
            planetasv=[p1,p2]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[4]=False
            if True in l:        
               l[l.index(True)]=False
            l[4]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[5]==True:
            dt=0.15
            combustible=100
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/12.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [300, 150], [0,14],50,im.p11)
            p2 = planeta(50, [100, 360], [0,10],50,im.p12)
            p3 = planeta(50, [200, 250], [0,15],50,im.p13)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]-(p1.tamaño)+18,p1.posicion[1]), [0,0],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[5]=False
            if True in l:        
               l[l.index(True)]=False
            l[5]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[6]==True:
            dt=0.15
            combustible=100
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/15.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [300, 250], [0,17],50,im.p14)
            p2 = planeta(50, [100, 250], [0,10],50,im.p15)
            p3 = planeta(50, [200, 250], [0,15],50,im.p16)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]-(p1.tamaño)+18,p1.posicion[1]), [0,0],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[6]=False
            if True in l:        
                l[l.index(True)]=False
            l[6]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[7]==True:
            dt=0.15
            combustible=100
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/18.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [300, 160], [0,13],50,im.p17)
            p2 = planeta(50, [900, 360], [-4,-15],50,im.p18)
            p3 = planeta(50, [200, 160], [0,14],50,im.p19)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[7]=False
            if True in l:        
                l[l.index(True)]=False
            l[7]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[8]==True:
            dt=0.15
            combustible=100
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/21.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [800, 400], [0,17],50,im.p20)
            p2 = planeta(50, [600, 500], [-25,10],50,im.p21)
            p3 = planeta(50, [800, 160], [0,20],50,im.p22)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[8]=False
            if True in l:        
                l[l.index(True)]=False
            l[8]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[9]==True:
            dt=0.15
            combustible=100
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/20.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [900, 360], [0,-15],50,im.p17)
            p2 = planeta(50, [300, 360], [0,15],50,im.p20)
            p3 = planeta(50, [600, 60], [-15,0],50,im.p23)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[9]=False
            if True in l:        
               l[l.index(True)]=False
            l[9]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[10]==True:
            dt=0.15
            combustible=100
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/6.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [600, 600], [-15,0],50,im.p24)
            p2 = planeta(50, [600, 100], [20,0],50,im.p6)
            p3 = planeta(50, [600, 500], [20,0],50,im.p4)
            p4 = planeta(50, [600, 0], [-15,0],50,im.p22)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[10]=False
            if True in l:        
               l[l.index(True)]=False
            l[10]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[11]==True:
            dt=0.15
            combustible=100
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/11.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [800, 360], [0,20],50,im.p14)
            p2 = planeta(50, [100, 360], [0,14],50,im.p11)
            p3 = planeta(50, [900, 360], [0,14],50,im.p16)
            p4 = planeta(50, [700, 360], [0,30],50,im.p12)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20+5), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[11]=False
            if True in l:        
               l[l.index(True)]=False
            l[11]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[12]==True:
            dt=0.15
            combustible=100
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/9.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [800, 360], [0,-20],50,im.p3)
            p2 = planeta(50, [100, 360], [0,14],50,im.p9)
            p3 = planeta(50, [900, 360], [0,20],50,im.p13)
            p4 = planeta(50, [700, 500], [-10,17],50,im.p8)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]+p1.tamaño/2-5,p1.posicion[1]), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[12]=False
            if True in l:        
               l[l.index(True)]=False
            l[12]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[13]==True:
            dt=0.15
            combustible=50
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/24.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [550, 250], [30,0],50,im.p18)
            p2 = planeta(50, [800, 100], [15,0],50,im.p24)
            p3 = planeta(50, [775, 150], [10,10],50,im.p11)
            p4 = planeta(50, [700, 200], [7,15],50,im.p16)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[13]=False
            if True in l:        
               l[l.index(True)]=False
            l[13]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[14]==True:
            dt=0.15
            combustible=50
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/7.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [900, 360], [0,-15],50,im.p6)
            p2 = planeta(50, [300, 360], [0,16],50,im.p7)
            p3 = planeta(50, [600, 60], [-17,0],50,im.p9)
            p4 = planeta(50, [600, 660], [18,0],50,im.p21)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[14]=False
            if True in l:        
               l[l.index(True)]=False
            l[14]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[15]==True:
            dt=0.15
            combustible=50
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/16.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [600, 250], [30,0],50,im.p14)
            p2 = planeta(50, [800, 100], [15,0],50,im.p16)
            p3 = planeta(50, [800, 300], [0,14],50,im.p21)
            p4 = planeta(50, [600, 660], [18,0],50,im.p11)
            p5 = planeta(50, [600, 10], [18,0],50,im.p24)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4,p5]
            planetasv=[p1,p2,p3,p4,p5]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[15]=False
            if True in l:        
                l[l.index(True)]=False
            l[15]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[16]==True:
            dt=0.15
            combustible=30
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/6.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [800, 360], [0,20],50,im.p5)
            p2 = planeta(50, [100, 360], [0,-10],50,im.p6)
            p3 = planeta(50, [900, 360], [0,-20],50,im.p3)
            p4 = planeta(50, [300, 360], [0,20],50,im.p9)
            p5 = planeta(50, [600, 550], [20,0],50,im.p24)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4,p5]
            planetasv=[p1,p2,p3,p4,p5]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[16]=False
            if True in l:        
                l[l.index(True)]=False
            l[16]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[17]==True:
            dt=0.15
            combustible=30
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/21.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [500, 360], [0,-30],50,im.p15)
            p2 = planeta(50, [700, 360], [0,30],50,im.p21)
            p3 = planeta(50, [755, 360], [0,23],50,im.p17)
            p4 = planeta(50, [445, 360], [0,-23],50,im.p11)
            p5 = planeta(50, [600, 150], [20,0],50,im.p19)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4,p5]
            planetasv=[p1,p2,p3,p4,p5]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[17]=False
            if True in l:        
                l[l.index(True)]=False
            l[17]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[18]==True:
            dt=0.3
            combustible=30
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/2.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e2)
            p1 = planeta(50, [500, 360], [0,-40],50,im.p22)
            p2 = planeta(50, [700, 360], [0,30],50,im.p2)
            p3 = planeta(50, [755, 360], [0,13],50,im.p7)
            p4 = planeta(50, [445, 360], [10,-35],50,im.p4)
            p5 = planeta(50, [600, 150], [20,0],50,im.p5)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4,p5]
            planetasv=[p1,p2,p3,p4,p5]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[18]=False
            if True in l:        
               l[l.index(True)]=False
            l[18]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1
            
        if nm1[19]==True:
            dt=0.3
            combustible=15
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/6.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(100, [600, 50], [15,10],50,im.p14)
            p2 = planeta(50, [600, 440], [-31.5,0],40,im.p6)
            p3 = planeta(50, [750, 360], [0,23],50,im.p7)
            p4 = planeta(50, [550, 490], [-25,0],50,im.p18)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+22), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm1[19]=False
            if True in l:        
               l[l.index(True)]=False
            l[19]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo1

        """ #########################################################"""
        """ #########################################################"""
        """ ######################## MUNDO 2 ########################"""
        """ #########################################################"""    
        """ #########################################################"""
        
        if nm2[0]==True:
            dt=0.3
            combustible=30
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/3.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(500, [900, 360], [0,-10],40,im.p1)
            p2 = planeta(500, [520, 360], [0,33],40,im.p3)
            p3 = planeta(500, [700, 100], [15,0],40,im.p2)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]+p1.tamaño/2-5,p1.posicion[1]), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[0]=False
            if True in l:
                l[l.index(True)]=False
            l[20]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
        if nm2[1]==True:
            dt=0.3
            combustible=20
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/6.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(500, [1200, 360], [0,-10],60,im.p4)
            p2 = planeta(500, [520, 360], [0,33],40,im.p6)
            p3 = planeta(500, [450, 360], [0,-25],50,im.p5)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]+p1.tamaño/2-5,p1.posicion[1]), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[1]=False
            if True in l:        
                l[l.index(True)]=False
            l[21]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[2]==True:
            dt=0.3
            combustible=20
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/7.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [600, 500], [20,0],40,im.p8)
            p2 = planeta(50, [600, 700], [10,0],40,im.p7)
            p3 = planeta(50, [600, 600], [15,0],40,im.p9)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[2]=False
            if True in l:        
                l[l.index(True)]=False
            l[22]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
              
        if nm2[3]==True:
            dt=0.3
            combustible=20
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/11.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [700, 360], [0,30],40,im.p10)
            p2 = planeta(50, [300, 360], [0,14],40,im.p11)
            p3 = planeta(50, [800, 360], [0,20],40,im.p12)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño/2+5), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[3]=False
            if True in l:        
               l[l.index(True)]=False
            l[23]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[4]==True:
            dt=0.3
            combustible=15
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/14.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [600, 280], [-32.5,0],40,im.p13)
            p2 = planeta(50, [1100, 360], [-10,10],40,im.p14)
            p3 = planeta(50, [700, 360], [0,30],40,im.p15)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño/2+5), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[4]=False
            if True in l:        
               l[l.index(True)]=False
            l[24]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[5]==True:
            dt=0.3
            combustible=15
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/17.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [200, 300], [0,14],35,im.p16)
            p2 = planeta(50, [600, 500], [30,0],35,im.p17)
            p3 = planeta(50, [600, 100], [15,0],35,im.p18)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño/2+0.5), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[5]=False
            if True in l:        
               l[l.index(True)]=False
            l[25]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[6]==True:
            dt=0.3
            combustible=20
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/20.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [200, 360], [0,14],35,im.p19)
            p2 = planeta(50, [600, 100], [15,0],35,im.p20)
            p3 = planeta(50, [600, 250], [-30,0],35,im.p21)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño/2), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[6]=False
            if True in l:        
                l[l.index(True)]=False
            l[26]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[7]==True:
            dt=0.3
            combustible=10
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/23.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [600, 285], [35,0],35,im.p22)
            p2 = planeta(50, [75, 100], [15,0],35,im.p23)
            p3 = planeta(50, [500, 300], [20,-20],35,im.p24)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño/2-5), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[7]=False
            if True in l:        
                l[l.index(True)]=False
            l[27]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[8]==True:
            dt=0.3
            combustible=15
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/7.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [600, 100], [20,0],35,im.p6)
            p2 = planeta(50, [600, 500], [-25,0],35,im.p7)
            p3 = planeta(50, [600, 200], [25,0],35,im.p21)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]+p1.tamaño/2+7,p1.posicion[1]), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[8]=False
            if True in l:        
                l[l.index(True)]=False
            l[28]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[9]==True:
            dt=0.3
            combustible=10
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/14.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [400, 250], [30,0],35,im.p16)
            p2 = planeta(50, [800, 100], [15,0],35,im.p14)
            p3 = planeta(50, [600, 500], [20,0],35,im.p11)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño/2), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[9]=False
            if True in l:        
               l[l.index(True)]=False
            l[29]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[10]==True:
            dt=0.6
            combustible=15
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/22.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [600, 250], [30,0],50,im.p5)
            p2 = planeta(50, [800, 100], [-19,0],50,im.p22)
            p3 = planeta(50, [500, 360], [0,-34],50,im.p24)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+25), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[10]=False
            if True in l:        
               l[l.index(True)]=False
            l[30]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[11]==True:
            dt=0.6
            combustible=10
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/12.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [600, 550], [20,0],50,im.p9)
            p2 = planeta(50, [600, 650], [15,0],50,im.p12)
            p3 = planeta(50, [600, 450], [30,0],50,im.p6)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3]
            planetasv=[p1,p2,p3]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[11]=False
            if True in l:        
               l[l.index(True)]=False
            l[31]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[12]==True:
            dt=0.6
            combustible=10
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/14.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [600, 550], [18,0],50,im.p11)
            p2 = planeta(50, [600, 650], [15,0],50,im.p14)
            p3 = planeta(50, [600, 480], [28,0],50,im.p15)
            p4 = planeta(50, [300,360], [5,15],50,im.p16)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[12]=False
            if True in l:        
               l[l.index(True)]=False
            l[32]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[13]==True:
            dt=0.6
            combustible=30
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/19.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [600, 250], [30,0],50,im.p18)
            p2 = planeta(50, [100, 360], [0,10],50,im.p19)
            p3 = planeta(50, [200, 300], [0,14],50,im.p20)
            p4 = planeta(50, [200, 400], [0,14],50,im.p21)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño/2), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[13]=False
            if True in l:        
               l[l.index(True)]=False
            l[33]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[14]==True:
            dt=0.6
            combustible=5
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/6.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(500, [600, 260], [30,0],50,im.p24)
            p2 = planeta(500, [600, 460], [-30,0],50,im.p6)
            p3 = planeta(500, [700, 360], [0,30],50,im.p21)
            p4 = planeta(500, [500, 360], [0,-30],50,im.p5)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño/2), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[14]=False
            if True in l:        
               l[l.index(True)]=False
            l[34]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[15]==True:
            dt=0.6
            combustible=10
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/9.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [900, 50], [10,20],50,im.p5)
            p2 = planeta(50, [700, 360], [0,-30],50,im.p14)
            p3 = planeta(50, [500, 360], [0,30],50,im.p21)
            p4 = planeta(50, [400, 360], [0,-20],50,im.p16)
            p5 = planeta(50, [800, 400], [0,-21],50,im.p11)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño/2+17), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4,p5]
            planetasv=[p1,p2,p3,p4,p5]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[15]=False
            if True in l:        
                l[l.index(True)]=False
            l[35]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[16]==True:
            dt=0.6
            combustible=12
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/14.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [900, 50], [10,20],50,im.p5)
            p2 = planeta(50, [700, 360], [0,-30],50,im.p14)
            p3 = planeta(50, [500, 360], [0,30],50,im.p21)
            p4 = planeta(50, [400, 360], [0,-20],50,im.p16)
            p5 = planeta(50, [800, 360], [0,20],50,im.p24)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]-18,p1.posicion[1]+p1.tamaño/2+25), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4,p5]
            planetasv=[p1,p2,p3,p4,p5]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[16]=False
            if True in l:        
                l[l.index(True)]=False
            l[36]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[17]==True:
            dt=0.6
            combustible=20
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/6.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [700, 460], [20,-12],50,im.p5)
            p2 = planeta(50, [600, 660], [20,0],50,im.p6)
            p3 = planeta(50, [700, 260], [-20,-10],50,im.p7)
            p4 = planeta(50, [400, 460], [10,17],50,im.p9)
            p5 = planeta(50, [715, 560], [20,0],50,im.p21)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4,p5]
            planetasv=[p1,p2,p3,p4,p5]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[17]=False
            if True in l:        
                l[l.index(True)]=False
            l[37]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[18]==True:
            dt=0.6
            combustible=20
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/14.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e3)
            p1 = planeta(50, [400, 160], [20,0],50,im.p11)
            p2 = planeta(50, [800, 560], [-20,0],50,im.p14)
            p3 = planeta(50, [750, 300], [10,20],50,im.p15)
            p4 = planeta(50, [350, 360], [0,-14],50,im.p16)
            p5 = planeta(50, [200, 360], [0,-10],50,im.p17)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+20), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4,p5]
            planetasv=[p1,p2,p3,p4,p5]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[18]=False
            if True in l:        
               l[l.index(True)]=False
            l[38]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        if nm2[19]==True:
            dt=0.9
            combustible=10
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/2.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e1)
            p1 = planeta(50, [700, 360], [0,30],35,im.p1)
            p2 = planeta(50, [750, 360], [0,25],35,im.p2)
            p3 = planeta(50, [800, 360], [0,20],35,im.p22)
            p4 = planeta(50, [850, 360], [0,18],35,im.p4)
            p5 = planeta(50, [900, 360], [0,16],35,im.p5)
            p6 = planeta(50, [950, 360], [0,14],35,im.p6)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño+55), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4,p5,p6]
            planetasv=[p1,p2,p3,p4,p5,p6]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm2[19]=False
            if True in l:        
               l[l.index(True)]=False
            l[39]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo2
            
        """ #########################################################"""
        """ #########################################################"""
        """ ######################## MUNDO 3 ########################"""
        """ #########################################################"""    
        """ #########################################################"""
        plax,play=600,360
        if nm3[0]==True:
            dt=0.9
            combustible=30
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/6.png")
            e1 = planeta(100000, [600, 360], [0,0],100,im.e1)
            p1 = planeta(450, [plax+85, play], [0,-37],35,im.p1)
            p2 = planeta(500, [plax+280, play], [0,17],25,im.p6)
            p3 = planeta(500, [plax+123, play], [0,-25],35,im.p5)
            p4 = planeta(500, [plax+240, play], [0,-18],35,im.p4)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]-p1.tamaño/2,p1.posicion[1]-p1.tamaño/2-6), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm3[0]=False
            if True in l:        
                l[l.index(True)]=False
            l[40]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo3
            
        if nm3[1]==True:
            dt=0.9
            combustible=30
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/24.png")
            e1 = planeta(300000, [600, 360], [0,0],100,im.e1)
            p1 = planeta(500, [plax, play+135], [50,0],35,im.p7)
            p2 = planeta(500, [plax, play+250], [35,0],25,im.p24)
            p3 = planeta(500, [plax-135, play], [0,34],35,im.p9)
            p4 = planeta(500, [plax-180, play], [0,34],35,im.p8)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]+20,p1.posicion[1]-p1.tamaño/2+10), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm3[1]=False
            if True in l:        
                l[l.index(True)]=False
            l[41]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo3
            
        if nm3[2]==True:
            dt=0.9
            combustible=30
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/11.png")
            e1 = planeta(300000, [600, 360], [0,0],100,im.e1)
            p1 = planeta(500, [plax, play+300], [20,0],35,im.p10)
            p2 = planeta(500, [plax, play-500], [15,0],25,im.p11)
            p3 = planeta(500, [plax+200, play], [0,24],35,im.p12)
            p4 = planeta(500, [plax+100, play], [0,54],35,im.p13)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño/2), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm3[2]=False
            if True in l:        
                l[l.index(True)]=False
            l[42]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo3
              
        if nm3[3]==True:
            dt=0.9
            combustible=30
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/15.png")
            e1 = planeta(300000, [600, 360], [0,0],100,im.e1)
            p1 = planeta(500, [plax, play+230], [25,0],35,im.p14)
            p2 = planeta(500, [plax, play-100], [45,0],25,im.p15)
            p3 = planeta(500, [plax-250, play], [0,30],35,im.p16)
            p4 = planeta(500, [plax+300, play], [0,29],35,im.p17)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]+2,p1.posicion[1]-p1.tamaño/2+2), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm3[3]=False
            if True in l:        
               l[l.index(True)]=False
            l[43]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo3
            
        if nm3[4]==True:
            dt=0.9
            combustible=30
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/19.png")
            e1 = planeta(300000, [600, 360], [0,0],100,im.e1)
            p1 = planeta(500, [plax, play+200], [30,0],35,im.p18)
            p2 = planeta(500, [plax, play+400], [25,0],25,im.p19)
            p3 = planeta(500, [plax, play+250], [30,0],35,im.p20)
            p4 = planeta(500, [plax, play+300], [30,0],35,im.p21)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]+2,p1.posicion[1]-p1.tamaño/2+2), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm3[4]=False
            if True in l:        
               l[l.index(True)]=False
            l[44]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo3
            
        if nm3[5]==True:
            dt=0.6
            combustible=30
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/23.png")
            e1 = planeta(900000, [600, 360], [0,0],100,im.e1)
            p1 = planeta(500, [plax-250, play], [0,60],35,im.p22)
            p2 = planeta(50, [plax-500, play], [0,29],25,im.p23)
            p3 = planeta(300, [plax-350, play], [0,34],35,im.p24)
            p4 = planeta(300, [plax-300, play], [0,34],35,im.p1)
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]+p1.tamaño/2+7), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm3[5]=False
            if True in l:        
               l[l.index(True)]=False
            l[45]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo3
            
        if nm3[6]==True:
            dt=0.6
            combustible=30
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/14.png")
            e1 = planeta(1000000, [600, 360], [0,0],100,im.e1)
            p1 = planeta(500, [plax+90, play], [0,100],35,im.p11)
            p2 = planeta(500, [plax+150, play], [0,90],25,im.p14)
            p3 = planeta(500, [plax+200, play], [0,80],35,im.p21)
            p4 = planeta(500, [plax+250, play], [0,70],35,im.p5)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]-20,p1.posicion[1]-p1.tamaño/2+100), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm3[6]=False
            if True in l:        
                l[l.index(True)]=False
            l[46]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo3
            
        if nm3[7]==True:
            dt=0.9
            combustible=30
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/7.png")
            e1 = planeta(1000000, [600, 360], [0,0],100,im.e1)
            p1 = planeta(500, [plax-100, play], [0,100],55,im.p6)
            p2 = planeta(500, [plax+300, play], [0,50],25,im.p7)
            p3 = planeta(500, [plax, play-100], [90,0],35,im.p9)
            p4 = planeta(500, [plax, play-300], [60,0],35,im.p14)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]+25,p1.posicion[1]-p1.tamaño/2+140), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm3[7]=False
            if True in l:        
                l[l.index(True)]=False
            l[47]=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo3
            
        if nm3[8]==True:
            dt=0.9
            combustible=30
            juego=True
            imp2=p1=pygame.image.load("imagenes/planets/19.png")
            e1 = planeta(1000000, [600, 360], [0,0],100,im.e1)
            p1 = planeta(500, [plax, play+100], [100,0],50,im.p18)
            p2 = planeta(500, [plax, play-100], [-100,0],25,im.p19)
            p3 = planeta(500, [plax, play+150], [85,0],35,im.p20)
            p4 = planeta(500, [plax, play-150], [-85,0],35,im.p21)
            COHETE=planeta(1*10**(-10), (p1.posicion[0]+120,p1.posicion[1]-70), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,p2,p3,p4]
            planetasv=[p1,p2,p3,p4]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm3[8]=False
            if True in l:        
                l[l.index(True)]=False
            l[48]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo3
            
        if nm3[9]==True:
            dt=0.9
            combustible=10
            juego=True
            plax, play=(600+600+150)/2,360
            imp2=p1=pygame.image.load("imagenes/planets/14.png")
            e1 = planeta(500000, [600, 360], [0,30],70,im.e1)
            e2 = planeta(500000, [600+150, 360], [0,-30],70,im.e1)
            
            p1 = planeta(50, [plax+300, play], [0,50],40,im.p11)
            p2 = planeta(50, [plax-300, play], [0,-50],25,im.p12)
            
            p3 = planeta(500, [plax, play+350], [-50,0],40,im.p13)
            p4 = planeta(500, [plax, play-350], [50,0],35,im.p14)
            
            p5 = planeta(500, [plax, play+400], [-50,0],40,im.p15)
            p6 = planeta(500, [plax, play-400], [50,0],35,im.p16)
            
            COHETE=planeta(1*10**(-10), (p1.posicion[0],p1.posicion[1]-p1.tamaño/2+75), [10,-4],10,im.e4)
            planetas= [COHETE,p1,e1,e2,p2,p3,p4,p5,p6]
            planetasv=[p1,p2,p3,p4,p5,p6]
            poscohete=(1,1)
            movimiento=False
            t=0
            nm3[9]=False
            if True in l:        
               l[l.index(True)]=False
            l[49]=True
            juego=True
            fondojuegox,fondojuegoy=0,0
            fondo_nivel=im.fondo_mundo3
            
        
        
        """ #########################################################"""
        """ #########################################################"""
        """ ####################### CONTROLES #######################"""
        """ #########################################################"""    
        """ #########################################################"""
        if click2==True:
            click_sostenido=False
        click2=False
        click=False
        
            
        #Eventos de mouse y teclado
        for event in pygame.event.get():
            if event.type == QUIT:
                file=open("save.txt","w")
                for i in avance:
                    file.write(str(i))   
                file.close()
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                """"### ESCAPE## """
                if event.key==pygame.K_ESCAPE:
                    if menu==True:
                        file=open("save.txt","w")
                        for i in avance:
                            file.write(str(i))   
                        file.close()
                        pygame.quit()
                        sys.exit()
                    elif menu2==True:
                        menu2=False
                        menu=True
                        ##intro
                        intro_old=None
                        xp1=ancho/2-170
                        yp1=alto/2-25+12
                        vp1=8
                        
                        xp2=ancho/2-300
                        yp2=alto/2-25+5
                        vp2=6
                        
                        xp3=ancho/2-500
                        yp3=alto/2-25
                        vp3=4
                    elif pausa==True:
                        juego=True
                        pausa=False
                    elif juego==True:
                        pausa=True
                        juego=False
                    elif mundo1==True:
                        menu2=True
                        mundo1=False
                    elif mundo2==True:
                        menu2=True
                        mundo2=False
                    elif mundo3==True:
                        menu2=True
                        mundo3=False
                    elif lost==True:
                        lost=False
                        menu2=True
                    elif como_jugar==True:
                        como_jugar=False
                        menu=True
                    elif siguiente2==True:
                        menu2=True
                        siguiente2=False
                    if ganar==True:
                        menu=True
                        ganar=False
                        juego=False
                        menu2=False
                    
                    if como_jugar==True or como_jugar2==True or como_jugar3==True or como_jugar4==True or como_jugar5==True:
                        como_jugar=False
                        como_jugar2=False
                        como_jugar3=False
                        como_jugar4=False
                        como_jugar5=False
                        menu=True

                """### FLECHAS ###"""
                if event.key==pygame.K_SPACE:
                    pygame.display.toggle_fullscreen()
                if event.key==pygame.K_LEFT:
                    if combustible>0:
                        LEFT=-1
                    if combustible==0:
                        LEFT=0
                if event.key==pygame.K_RIGHT:
                    if combustible>0:
                        RIGHT=1
                    if combustible==0:
                        RIGHT=0
                if event.key==pygame.K_DOWN:
                    if combustible>0:
                        DOWN=1
                    if combustible==0:
                        DOWN=0
                if event.key==pygame.K_UP:
                    if combustible>0:
                        UP=-1
                    if combustible==0:
                        UP=0
                """"### R ### """
                if event.key==pygame.K_r:
                    if ganar==False:
                        if juego==True or lost==True or siguiente_nivel==True:
                            pygame.mixer.Sound.play(s.click)
                            click=False
                            xinicial,yinicial=mousex,mousey
                            COHETE.posicion[0]=-100
                            COHETE.posicion[1]=-100
                            siguiente_nivel=False
                            lost=False
                            if True in l:
                                if 0<=l.index(True)<20:
                                    nm1[l.index(True)]=True
                                elif 20<=l.index(True)<40:
                                    nm2[l.index(True)-20]=True
                                elif 40<=l.index(True)<60:
                                    nm3[l.index(True)-40]=True
                            juego=True
                """### P ###"""
                if event.key==pygame.K_p:
                    if juego==True:
                        pausa=True
                        juego=False
                    elif pausa==True:
                        pausa=False
                        juego=True
                
            elif event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT:
                    LEFT=0
                elif event.key==pygame.K_RIGHT:
                    RIGHT=0
                elif event.key==pygame.K_DOWN:
                    DOWN=0
                elif event.key==pygame.K_UP:
                    UP=0
                    
            elif event.type==MOUSEMOTION:
                mousex,mousey=event.pos
            elif event.type==MOUSEBUTTONDOWN:
               click=True
               click_sostenido=True
               mousex,mousey=event.pos  
               mousesx,mousesy=event.pos
            elif event.type==MOUSEBUTTONUP:
                mousex,mousey=event.pos
                click2=True

        """ #########################################################"""
        """ #########################################################"""
        """ ######################### MENUS #########################"""
        """ #########################################################"""    
        """ #########################################################"""
        #menu
        if menu==True:
            #Teclas
            UP,DOWN,RIGHT,LEFT="falso","falso","falso","falso"
            
            if intro_old is None:
                pantalla1=pantalla.blit(fondo1,(pos_fondo,0))
                pantalla2=pantalla.blit(fondo1,(pos_fondo-1280,0))
            else:
                pantalla1=pantalla.blit(fondo1,intro_old,intro_old)
                pantalla2=pantalla.blit(fondo1,intro_old,intro_old)
                
            if pos_fondo>1280:
                pos_fondo=0
            pos_fondo=pos_fondo+vel_fondo

            if pygame.mixer.music.get_busy()==False:
                musica_menu=pygame.mixer.music.load("sonidos/principal/TheySay-menu.mp3")
                pygame.mixer.music.play(-1,0,239)
            
            #intro
            planeta1=intro.planeta1
            planeta2=intro.planeta2
            planeta3=intro.planeta3
            """
            planeta1=im.p21
            planeta2=im.p7
            planeta3=im.p6"""
            #sol=intro.sol
            sol=pygame.transform.scale(im.e2,(200,200))
            tamañoplaneta=intro.tamañoplaneta
            
            xp1=xp1+vp1
            absvp1=vp1/abs(vp1)
            xp2=xp2+vp2
            absvp2=vp2/abs(vp2)
            xp3=xp3+vp3
            absvp3=vp3/abs(vp3)
            
            if vp3<0:
                vp3=vp3*1.0005
                pantalla.blit(planeta3,(xp3,yp3))
            if vp2<0:
                vp2=vp2*1.0005  
                pantalla.blit(planeta2,(xp2,yp2))
            if vp1<0.1:
                vp1=vp1*1
                pantalla.blit(planeta1,(xp1,yp1))
            
                              
            pantalla.blit(sol,(ancho/2-500+125,alto/2-215+100))
            
            if vp1>0:
                vp1=vp1/1
                pantalla.blit(planeta1,(xp1,yp1))
            if vp2>0:
                vp2=vp2/1.0005
                pantalla.blit(planeta2,(xp2,yp2))
            if vp3>0:
                vp3=vp3/1.0005
                pantalla.blit(planeta3,(xp3,yp3))
            
            
            if xp1>ancho-800 or xp1<0+200:
                vp1=-vp1
            if xp2>ancho-700 or xp2<0+100:
                vp2=-vp2
            if xp3>ancho-600 or xp3<0+50:
                vp3=-vp3
            
            #fondo dentro del juego 
            fondojuegox,fondojuegoy=-(fond/2)+1280/2,-(fond/2)+720/2
    
            
            #boton de jugar
            pos_b_playx,pos_b_playy=(ancho/2)+250,(alto/2)-50
            
            b_play=boton(im.b_jugar,im.bo_jugar,pos_b_playx,pos_b_playy)
            if cursor.colliderect(b_play.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                menu=False
                menu2=True
                pantalla.blit(fondo1,(0,0))
                click=False
                
            #boton de como jugar
            b_como_jugar=boton(im.b_como_jugar,im.bo_como_jugar,pos_b_playx,pos_b_playy+75)
            if cursor.colliderect(b_como_jugar.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                menu=False
                como_jugar=True
                click=False
            #boton de salir
            b_salir=boton(im.b_salir,im.bo_salir,pos_b_playx,pos_b_playy+150)                            
            if cursor.colliderect(b_salir.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                file=open("save.txt","w")
                for i in avance:
                    file.write(str(i))   
                file.close()
                time.sleep(0.1)
                pygame.quit()
                sys.exit()    
            

            #actualizacion botones menu
            b_play.update(pantalla, cursor)
            b_salir.update(pantalla,cursor)
            b_como_jugar.update(pantalla,cursor)
        
        
        
            
        
        #Pausa
        pospausax,pospausay=498,340
        if pausa==True:
            pantalla.blit(fondo_nivel,(fondojuegox, fondojuegoy))
            pygame.draw.rect(pantalla, c.darkslateblue, [390, 90, 500,500])
            texto("Pausa",75,540,75+40,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
             # VOLUMEN DE LA MUSICA
            #texto("Musica",35,310+65,335-147,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            pantalla.blit(im.music,(447,242-50+40))
            musica=slider(pygame.transform.scale(im.des1,(300,40)),im.des2,450+40,350-150+40,posvolx+40,350-150+40,c.royalblue)
            musica.update(pantalla, cursor)
            texto(str(int(vol*100)),30,858-65,343-150+40,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            
            if deslizador==1:
                posvolx=mousex-45 #145
                if posvolx<451:
                    posvolx=450
                    vol=0
                elif mousex>=451 and mousex<595:
                    vol=0.25
                elif mousex>=595 and mousex<667.5:
                    vol=0.5
                elif mousex>667.5 and mousex<780:
                    vol=0.75
                elif mousex>785:#760:
                    posvolx=740
                    vol=1
                pygame.mixer.music.set_volume(vol)
                                              
            # VOLUMEN DE LOS EFECTOS DE SONIDO
            #texto("Sonidos",35,300+65,325+60-147,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            pantalla.blit(im.sound,(450,242+40))
            volumen=slider(pygame.transform.scale(im.des1,(300,40)),im.des2,450+40,350+50-150+40,possonx+40,350+50-150+40,c.royalblue)
            volumen.update(pantalla, cursor)
            texto(str(int(sound*100)),30,858-65,343+50-150+40,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            
            if deslizador==1:
                possonx=mousex-45
                if possonx<451:
                    possonx=450
                    sound=0
                elif mousex>=451 and mousex<595:
                    sound=0.25
                elif mousex>=595 and mousex<667.5:
                    sound=0.5
                elif mousex>657.5 and mousex<780:
                    sound=0.75
                elif mousex>785:
                    possonx=740
                    sound=1
                pygame.mixer.Sound.set_volume(s.click,sound)
                
            
            b_reanudar=boton(im.b_reanudar,im.bo_reanudar,pospausax,pospausay)
            if cursor.colliderect(b_reanudar.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                juego=True
                click=False
                pausa=False
                xinicial,yinicial=mousex,mousey
            
            b_pausa=boton(im.b_menu,im.bo_menu,pospausax,pospausay+140)
            if cursor.colliderect(b_pausa.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                juego=False
                click=False
                pausa=False
                xinicial,yinicial=mousex,mousey
                if pmundo1==True:
                    for m in nm1:
                        m=False
                    mundo1=True
                if pmundo2==True:
                    for m in nm2:
                        m=False
                    mundo2=True 
                if pmundo3==True:
                    for m in nm3:
                        m=False
                    mundo3=True 
            
            b_pausa2=boton(im.b_reiniciar,im.bo_reiniciar,pospausax,pospausay+70)
            if cursor.colliderect(b_pausa2.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                juego=False
                click=False
                pausa=False
                xinicial,yinicial=mousex,mousey
                if True in l:
                    if 0<=l.index(True)<20:
                        nm1[l.index(True)]=True
                    elif 20<=l.index(True)<40:
                        nm2[l.index(True)-20]=True
                    elif 40<=l.index(True)<60:
                        nm3[l.index(True)-40]=True
                juego=True
            
            
               
            #actualizacion botones pausa
            b_pausa.update(pantalla, cursor)
            b_pausa2.update(pantalla, cursor)
            b_reanudar.update(pantalla, cursor)

        #lost
        if lost==True:
            pantalla.blit(fondo_nivel,(fondojuegox, fondojuegoy))
            #Colocar la imagen de cada planeta en pantalla                              
            
            pygame.draw.rect(pantalla, c.darkslateblue, [400, 115, 500,450])
            texto("La agonizante vida",50,433,160,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("de tus tripulantes",50,433,210,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("ha llegado a su fin",50,433,260,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            
            b_reiniciar=boton(im.b_reiniciar,im.bo_reiniciar,pospausax,pospausay+15)
            if cursor.colliderect(b_reiniciar.rect) and click==True:
                lost=False
                pygame.mixer.Sound.play(s.click)
                click=False
                xinicial,yinicial=mousex,mousey
                #juego=False
                COHETE.posicion[0]=-100
                COHETE.posicion[1]=-100
                if True in l:
                    if 0<=l.index(True)<20:
                        nm1[l.index(True)]=True
                    elif 20<=l.index(True)<40:
                        nm2[l.index(True)-20]=True
                    elif 40<=l.index(True)<60:
                        nm3[l.index(True)-40]=True
                juego=True
        
            
            b_volver_m2=boton(im.b_menu,im.bo_menu,pospausax,pospausay+70+15)
            if cursor.colliderect(b_volver_m2.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                click=False
                lost=False
                xinicial,yinicial=mousex,mousey
                if pmundo1==True:
                    for m in nm1:
                        m=False
                    mundo1=True
                elif pmundo2==True:
                    for m in nm2:
                        m=False
                    mundo2=True 
                elif pmundo3==True:
                    for m in nm3:
                        m=False
                    mundo3=True
            #actualizacion botones lost
            b_volver_m2.update(pantalla, cursor)
            b_reiniciar.update(pantalla, cursor)
        """ #########################################################"""
        """ #########################################################"""
        """ ######################### JUEGO #########################"""
        """ #########################################################"""    
        """ #########################################################"""
        
        
        if juego==True and menu2==False:  
            lost=False
            if pygame.key.get_focused()==0:
                pausa=True
                juego=False
                
            #if p2 in planetasv:
             #   planetasv.pop(planetasv.index(p2))
            #calcular el centro de un planeta y su distancia al cohete
            for m in planetas:
                m.centro=m.posicion-(COHETE.tamaño/2,COHETE.tamaño/2)
                m.cohete=np.sqrt(((m.centro[0])-(COHETE.posicion[0]))**2+((m.centro[1])-(COHETE.posicion[1]))**2)
            for m in planetas:
                m.e1=m.posicion-(e1.tamaño/2,e1.tamaño/2)
                m.e1=np.sqrt(((m.centro[0])-(e1.posicion[0]))**2+((m.centro[1])-(e1.posicion[1]))**2)
            if e2 in planetas:
                for m in planetas:
                    m.e2=m.posicion-(e2.tamaño/2,e2.tamaño/2)
                    m.e2=np.sqrt(((m.centro[0])-(e2.posicion[0]))**2+((m.centro[1])-(e2.posicion[1]))**2)
            
            # Calcular sumatoria de fuerzas sobre un cuerpo 
            for m in planetas:
                m.fuerza = np.array((0,0))
                for n in planetas:
                    if n == m:
                        continue
                    else: m.fuerza = m.fuerza + m.fuerzag(n)
        
            # Actualizar momenta
            for m in planetas:
                m.momentum = m.momentum + (m.fuerza * dt)
            
            # Detectar colisiones planeta-planeta y fusionarlos

            
            for m in planetasv:
                for n in planetasv:
                    distancia = math.hypot(m.posicion[0]-n.posicion[0],m.posicion[1]-n.posicion[1])
                    if m == p1: continue
                    if distancia <= (m.tamaño/2) + (n.tamaño/2)+2  and m!=n:
                        explosion=explosiones(((n.centro[0]+m.centro[0])/2,(n.centro[1]+m.centro[1])/2),'t4')
                        Explosiones.add(explosion)
                        planetasv.remove(m)
                        planetas.remove(m)
                        m.kill()
                        n.masa = m.masa + n.masa
                        n.momentum = m.momentum + n.momentum  
                        n.imagen=im.p0
                        

    
            # Detectar colisiones planeta-estrella y fusionarlos
            for n in planetasv:
                distancia = math.hypot(e1.posicion[0] - n.posicion[0], e1.posicion[1] - n.posicion[1])
                if distancia <= (e1.tamaño/2) + (n.tamaño/2):
                    explosion=explosiones(((n.centro[0]+e1.centro[0])/2,(n.centro[1]+e1.centro[1])/2),'t2')
                    Explosiones.add(explosion)
                    planetasv.remove(n)
                    planetas.remove(n)
                    n.kill()
                    e1.masa = e1.masa + n.masa
                    e1.momentum = e1.momentum + n.momentum
                    if p2.e1<p2.tamaño/2+p2.tamaño/2:
                        p2.posicion[0],p2.posicion[1]=10**1,10**1
                        
            # Actualizar posiciones de planetas
            for m in planetas:
                m.posicion = m.posicion + m.momentum / m.masa * dt

            
            if UP=="falso" and DOWN=="falso" and LEFT=="falso" and RIGHT=="falso": #si no se ha oprimido ninguna tecla
                cp1=COHETE.posicion-p1.posicion
                COHETE.posicion=p1.centro+(0,p1.tamaño/2)+(18,0)
                COHETE.momentum=(p1.momentum/p1.masa)*COHETE.masa

            
            if UP!="falso" or DOWN!="falso" or RIGHT!="falso" or LEFT!="falso": #Si se oprime una tecla
                if UP=="falso" or DOWN=="falso" or RIGHT=="falso" or LEFT=="falso":
                    UP,DOWN,RIGHT,LEFT=0,0,0,0
                    COHETE.posicion=COHETE.posicion
                if combustible>0:
                    COHETE.momentum=COHETE.momentum+[(LEFT+RIGHT)/10**10,(DOWN+UP)/10**10] 
            
            
            for m in planetas:
                m.centro=m.posicion-(COHETE.tamaño/2,COHETE.tamaño/2)
                m.cohete=np.sqrt(((m.centro[0])-(COHETE.posicion[0]))**2+((m.centro[1])-(COHETE.posicion[1]))**2)
            
            for m in planetasv:
                if m.cohete<m.tamaño/2+COHETE.tamaño/2+6:
                    if m.cohete>m.tamaño/2+COHETE.tamaño/2:
                        movimiento=False
                    if m.cohete<m.tamaño/2+COHETE.tamaño/2:
                        COHETE.momentum=(m.momentum/m.masa)*COHETE.masa
                        if movimiento==False:
                            poscohete=COHETE.posicion-m.centro
                            if poscohete[0]<0:
                                poscohete[0]=poscohete[0]+COHETE.tamaño/20
                            else:
                                poscohete[0]=poscohete[0]+COHETE.tamaño/20
                            if poscohete[1]<0:
                                poscohete[1]=poscohete[1]-COHETE.tamaño/20
                            else:
                                poscohete[1]=poscohete[1]+COHETE.tamaño/20
                            movimiento=True
                        if UP==0 and DOWN==0 and LEFT==0 and RIGHT==0:
                            COHETE.posicion=m.centro+poscohete
                        if COHETE.posicion[0]-m.posicion[0]<0 and LEFT==-1:
                                COHETE.posicion[0]=COHETE.posicion[0]-3
                        if COHETE.posicion[0]-m.posicion[0]>0 and RIGHT==1:
                                COHETE.posicion[0]=COHETE.posicion[0]+3
                        if COHETE.posicion[1]-m.posicion[1]<0 and UP==-1:
                                COHETE.posicion[1]=COHETE.posicion[1]-3
                        if COHETE.posicion[1]-m.posicion[1]>0 and DOWN==1:
                                COHETE.posicion[1]=COHETE.posicion[1]+3
            
            
            #actualizar combustible
            if combustible>0:
                if RIGHT==1 or LEFT==-1 or UP==-1 or DOWN==1:
                    combustible=combustible-1  
            
            # menu de lost al caer en la estrella
            if e1.cohete<e1.tamaño/2+6:
                juego=False
                lost=True
            if e2 in planetas:
                if e2.cohete<e2.tamaño/2+6:
                    juego=False
                    lost=True
                for n in planetasv:
                    distancia = math.hypot(e2.posicion[0] - n.posicion[0], e2.posicion[1] - n.posicion[1])
                    if distancia <= (e2.tamaño/2) + (n.tamaño/2):
                        explosion=explosiones(((n.centro[0]+e2.centro[0])/2,(n.centro[1]+e2.centro[1])/2),'t2')
                        Explosiones.add(explosion)
                        planetasv.remove(n)
                        planetas.remove(n)
                        n.kill()
                        e2.masa = e2.masa + n.masa
                        e2.momentum = e2.momentum + n.momentum
                        if p2.e2<p2.tamaño/2+p2.tamaño/2:
                            p2.posicion[0],p2.posicion[1]=10**1,10**1
            #Iniciar cada frame completamente negro
            pantalla.fill((0,0,0))
            l1=l[0:20]
            l2=l[20:39]
            l3=l[40:60]

            pantalla.blit(fondo_nivel,(fondojuegox, fondojuegoy))

            #Colocar la imagen de cada planeta en pantalla                              
            for m in planetas:
                if m!=COHETE:
                    pantalla.blit(m.im(), m.posicion-(m.tamaño/2,m.tamaño/2))

            pantalla.blit(COHETE.im(), COHETE.posicion)
            
            
            #actualizar el tiempo transcurrido
            t = round(t + dt,10)
            
            #mover el fondo
            if click==True or int(t/dt)%3==0:
                xinicial,yinicial=mousex,mousey
            if click_sostenido==True:
                for m in planetas:
                        m.posicion=m.posicion+[(mousex-xinicial),(mousey-yinicial)]
                        
            #actualizar lost si p2 no esta
            if p2 in planetas: pass
            else:
                lost=True
                juego=False
            """########################################################"""
            """#################### TEXTOS EN JUEGO ####################"""
            """########################################################"""
            color_boton_juego=c.midnightblue
            pygame.draw.rect(pantalla, color_boton_juego, [1100,30,150,100])

            comb=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/combustible.png"),(35,35))
            icono_vel=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/icono_vel.png"),(35,35))
            pantalla.blit(comb,(1110,40))
            
            texto(str(combustible),40,1150,37,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            #Velocidad
            pantalla.blit(icono_vel,(1110,80))
            #texto("Velocidad",30,1050,70,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            for m in planetas:
                if m.cohete<m.tamaño/2+COHETE.tamaño/2:
                    vel_cohete=0
                else:
                    vel_cohete=0
                    vel_cohete=dt*np.sqrt(COHETE.momentum[0]**2+COHETE.momentum[1]**2)/COHETE.masa
                if p1.cohete<p1.tamaño/2+COHETE.tamaño/2:
                    vel_cohete=0
                if COHETE.posicion[0]==0 and COHETE.posicion[1]==0:
                    vel_cohete=0
            for m in planetasv:
                if m.cohete<m.tamaño/2+COHETE.tamaño/2+1:
                    vel_cohete=0
            if t<5:
                texto(str(0),40,1150,80,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            else:
                texto(str(round(vel_cohete,1)),40,1150,80,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            #posicion
            #texto(str(int(COHETE.posicion[0])),30,1050,150,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            #texto(str(int(COHETE.posicion[1])),30,1050,200,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            #objetivo
            pygame.draw.rect(pantalla, color_boton_juego, [25,25,100,100])
            pantalla.blit(pygame.transform.scale(imp2,(75,75)),(37.5,37.5))
            
            #actualizar pantalla
            pygame.display.update()
            
            
        """ #########################################################"""
        """ #########################################################"""
        """ ######################### MENU 2 ########################"""
        """ #########################################################"""    
        """ #########################################################"""
        if menu2==True:
            pmundo1,pmundo2,pmundo3=False,False,False
            UP,DOWN,RIGHT,LEFT="falso","falso","falso","falso"
            
            if intro_old is None:
                pantalla1=pantalla.blit(fondo1,(pos_fondo,0))
                pantalla2=pantalla.blit(fondo1,(pos_fondo-1280,0))
            else:
                pantalla1=pantalla.blit(fondo1,intro_old,intro_old)
                pantalla2=pantalla.blit(
                    fondo1,intro_old,intro_old)

            if pos_fondo>1280:
                pos_fondo=0
            pos_fondo=pos_fondo+vel_fondo

            
            
            #fondo dentro del juego 
            fondojuegox,fondojuegoy=-(fond/2)+1280/2,-(fond/2)+720/2
    
            #b_lv=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/blanco.png"),(int((2*ancho)/10),int(alto/2)))
            #boton de mundo 1
            pos_b_mundosx,pos_b_mundosy=(ancho/10),(alto/4)
            b_mundo1=boton(im.b_mundo1,im.bo_mundo1,pos_b_mundosx,pos_b_mundosy)
            if cursor.colliderect(b_mundo1.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                click=False
                menu2=False
                mundo1=True
                
            #boton de mundo2
            b_mundo2=boton(im.b_mundo2,im.bo_mundo2,pos_b_mundosx+(3*ancho)/10,pos_b_mundosy)
            if cursor.colliderect(b_mundo2.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                click=False
                menu2=False
                mundo2=True
                
            #boton de mundo3
            b_mundo3=boton(im.b_mundo3,im.bo_mundo3,pos_b_mundosx+(6*ancho)/10,pos_b_mundosy)                            
            if cursor.colliderect(b_mundo3.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                click=False
                menu2=False
                mundo3=True
                
            #actualizacion botones menu2
            b_mundo1.update(pantalla, cursor)
            b_mundo2.update(pantalla,cursor)
            b_mundo3.update(pantalla,cursor)
            
        """ #########################################################"""
        """ #########################################################"""
        """ ######################## MUNDO 1 ########################"""
        """ #########################################################"""    
        """ #########################################################"""
        if mundo1==True:
            UP,DOWN,RIGHT,LEFT="falso","falso","falso","falso"
            pmundo1=True
            
            if intro_old is None:
                pantalla1=pantalla.blit(im.fondo_mundo1,(pos_fondo,0))
                pantalla2=pantalla.blit(im.fondo_mundo1,(pos_fondo-1280,0))
            else:
                pantalla1=pantalla.blit(im.fondo_mundo1,intro_old,intro_old)
                pantalla2=pantalla.blit(im.fondo_mundo1,intro_old,intro_old)

            if pos_fondo>1280:
                pos_fondo=0
            pos_fondo=pos_fondo+vel_fondo

            
            
            #fondo dentro del juego 
            fondojuegox,fondojuegoy=-(fond/2)+1280/2,-(fond/2)+720/2
    
            #b_lv=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/blanco.png"),(int((2*ancho)/10),int(alto/2)))
            
            #POSICION INICIAL
            pos_b_mundosx,pos_b_mundosy=(ancho/10),(alto/4)
           
            """############# BOTONES NIVELES MUNDO 1 ############"""
            sepx=175
            sepy=125
            pos_nivelesx=ancho/5
            pos_nivelesy=alto/5
            
            
            b_lv1=boton(im.b_niveles[0],im.bo_niveles[0],pos_nivelesx,pos_nivelesy)
            b_lv2=boton(im.b_niveles[1],im.bo_niveles[1],pos_nivelesx+sepx,pos_nivelesy)
            b_lv3=boton(im.b_niveles[2],im.bo_niveles[2],pos_nivelesx+sepx*2,pos_nivelesy)
            b_lv4=boton(im.b_niveles[3],im.bo_niveles[3],pos_nivelesx+sepx*3,pos_nivelesy)
            b_lv5=boton(im.b_niveles[4],im.bo_niveles[4],pos_nivelesx+sepx*4,pos_nivelesy)
            b_lv6=boton(im.b_niveles[5],im.bo_niveles[5],pos_nivelesx,pos_nivelesy+sepy)
            b_lv7=boton(im.b_niveles[6],im.bo_niveles[6],pos_nivelesx+sepx,pos_nivelesy+sepy)
            b_lv8=boton(im.b_niveles[7],im.bo_niveles[7],pos_nivelesx+sepx*2,pos_nivelesy+sepy)
            b_lv9=boton(im.b_niveles[8],im.bo_niveles[8],pos_nivelesx+sepx*3,pos_nivelesy+sepy)
            b_lv10=boton(im.b_niveles[9],im.bo_niveles[9],pos_nivelesx+sepx*4,pos_nivelesy+sepy)
            b_lv11=boton(im.b_niveles[10],im.bo_niveles[10],pos_nivelesx,pos_nivelesy+sepy*2)
            b_lv12=boton(im.b_niveles[11],im.bo_niveles[11],pos_nivelesx+sepx,pos_nivelesy+sepy*2)
            b_lv13=boton(im.b_niveles[12],im.bo_niveles[12],pos_nivelesx+sepx*2,pos_nivelesy+sepy*2)
            b_lv14=boton(im.b_niveles[13],im.bo_niveles[13],pos_nivelesx+sepx*3,pos_nivelesy+sepy*2)
            b_lv15=boton(im.b_niveles[14],im.bo_niveles[14],pos_nivelesx+sepx*4,pos_nivelesy+sepy*2)
            b_lv16=boton(im.b_niveles[15],im.bo_niveles[15],pos_nivelesx,pos_nivelesy+sepy*3)
            b_lv17=boton(im.b_niveles[16],im.bo_niveles[16],pos_nivelesx+sepx,pos_nivelesy+sepy*3)
            b_lv18=boton(im.b_niveles[17],im.bo_niveles[17],pos_nivelesx+sepx*2,pos_nivelesy+sepy*3)
            b_lv19=boton(im.b_niveles[18],im.bo_niveles[18],pos_nivelesx+sepx*3,pos_nivelesy+sepy*3)
            b_lv20=boton(im.b_niveles[19],im.bo_niveles[19],pos_nivelesx+sepx*4,pos_nivelesy+sepy*3)
            
            if cursor.colliderect(b_lv1.rect) and click==True and avance[0]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[0]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv2.rect) and click==True and avance[1]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[1]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv3.rect) and click==True and avance[2]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[2]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv4.rect) and click==True and avance[3]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[3]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv5.rect) and click==True and avance[4]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[4]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv6.rect) and click==True and avance[5]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[5]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv7.rect) and click==True and avance[6]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[6]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv8.rect) and click==True and avance[7]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[7]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv9.rect) and click==True and avance[8]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[8]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv10.rect) and click==True and avance[9]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[9]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv11.rect) and click==True and avance[10]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[10]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv12.rect) and click==True and avance[11]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[11]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv13.rect) and click==True and avance[12]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[12]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv14.rect) and click==True and avance[13]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[13]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv15.rect) and click==True and avance[14]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[14]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv16.rect) and click==True and avance[15]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[15]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv17.rect) and click==True and avance[16]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[16]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv18.rect) and click==True and avance[17]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[17]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv19.rect) and click==True and avance[18]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[18]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv20.rect) and click==True and avance[19]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo1=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm1[19]=True
                LEFT=0.00001
                
            #actualizacion botones menu2
            b_lv1.update(pantalla, cursor)
            b_lv2.update(pantalla, cursor)
            b_lv3.update(pantalla, cursor)
            b_lv4.update(pantalla, cursor)
            b_lv5.update(pantalla, cursor)
            b_lv6.update(pantalla, cursor)
            b_lv7.update(pantalla, cursor)
            b_lv8.update(pantalla, cursor)
            b_lv9.update(pantalla, cursor)
            b_lv10.update(pantalla, cursor)
            b_lv11.update(pantalla, cursor)
            b_lv12.update(pantalla, cursor)
            b_lv13.update(pantalla, cursor)
            b_lv14.update(pantalla, cursor)
            b_lv15.update(pantalla, cursor)
            b_lv16.update(pantalla, cursor)
            b_lv17.update(pantalla, cursor)
            b_lv18.update(pantalla, cursor)
            b_lv19.update(pantalla, cursor)
            b_lv20.update(pantalla, cursor)
            
            av1=avance[0:5]
            av2=avance[5:10]
            av3=avance[10:15]
            av4=avance[15:20]
            for i in av1:
                for n in range(5):
                    if avance[n]==0:
                        pantalla.blit(im.bb_niveles[n],(pos_nivelesx+sepx*n,pos_nivelesy))
            for i in av2:
                for n in range(5):
                    if avance[n+5]==0:
                        pantalla.blit(im.bb_niveles[n+5],(pos_nivelesx+sepx*n,pos_nivelesy+sepy*1))
            for i in av3:
                for n in range(5):
                    if avance[n+10]==0:
                        pantalla.blit(im.bb_niveles[n+10],(pos_nivelesx+sepx*n,pos_nivelesy+sepy*2))
            for i in av4:
                for n in range(5):
                    if avance[n+15]==0:
                        pantalla.blit(im.bb_niveles[n+15],(pos_nivelesx+sepx*n,pos_nivelesy+sepy*3))

        """ #########################################################"""
        """ #########################################################"""
        """ ######################## MUNDO 2 ########################"""
        """ #########################################################"""    
        """ #########################################################"""
        if mundo2==True:
            UP,DOWN,RIGHT,LEFT="falso","falso","falso","falso"
            pmundo2=True
            
            if intro_old is None:
                pantalla1=pantalla.blit(im.fondo_mundo2,(pos_fondo,0))
                pantalla2=pantalla.blit(im.fondo_mundo2,(pos_fondo-1280,0))
            else:
                pantalla1=pantalla.blit(im.fondo_mundo2,intro_old,intro_old)
                pantalla2=pantalla.blit(im.fondo_mundo2,intro_old,intro_old)

            if pos_fondo>1280:
                pos_fondo=0
            pos_fondo=pos_fondo+vel_fondo

            
            
            #fondo dentro del juego 
            fondojuegox,fondojuegoy=-(fond/2)+1280/2,-(fond/2)+720/2
    
            
            
            #POSICION INICIAL
            pos_b_mundosx,pos_b_mundosy=(ancho/10),(alto/4)
           
            """############# BOTONES NIVELES MUNDO 2 ############"""
            sepx=175
            sepy=125
            pos_nivelesx=ancho/5
            pos_nivelesy=alto/5
            b_lv21=boton(im.b_niveles[20],im.bo_niveles[20],pos_nivelesx,pos_nivelesy)
            b_lv22=boton(im.b_niveles[21],im.bo_niveles[21],pos_nivelesx+sepx,pos_nivelesy)
            b_lv23=boton(im.b_niveles[22],im.bo_niveles[22],pos_nivelesx+sepx*2,pos_nivelesy)
            b_lv24=boton(im.b_niveles[23],im.bo_niveles[23],pos_nivelesx+sepx*3,pos_nivelesy)
            b_lv25=boton(im.b_niveles[24],im.bo_niveles[24],pos_nivelesx+sepx*4,pos_nivelesy)
            b_lv26=boton(im.b_niveles[25],im.bo_niveles[25],pos_nivelesx,pos_nivelesy+sepy)
            b_lv27=boton(im.b_niveles[26],im.bo_niveles[26],pos_nivelesx+sepx,pos_nivelesy+sepy)
            b_lv28=boton(im.b_niveles[27],im.bo_niveles[27],pos_nivelesx+sepx*2,pos_nivelesy+sepy)
            b_lv29=boton(im.b_niveles[28],im.bo_niveles[28],pos_nivelesx+sepx*3,pos_nivelesy+sepy)
            b_lv30=boton(im.b_niveles[29],im.bo_niveles[29],pos_nivelesx+sepx*4,pos_nivelesy+sepy)
            b_lv31=boton(im.b_niveles[30],im.bo_niveles[30],pos_nivelesx,pos_nivelesy+sepy*2)
            b_lv32=boton(im.b_niveles[31],im.bo_niveles[31],pos_nivelesx+sepx,pos_nivelesy+sepy*2)
            b_lv33=boton(im.b_niveles[32],im.bo_niveles[32],pos_nivelesx+sepx*2,pos_nivelesy+sepy*2)
            b_lv34=boton(im.b_niveles[33],im.bo_niveles[33],pos_nivelesx+sepx*3,pos_nivelesy+sepy*2)
            b_lv35=boton(im.b_niveles[34],im.bo_niveles[34],pos_nivelesx+sepx*4,pos_nivelesy+sepy*2)
            b_lv36=boton(im.b_niveles[35],im.bo_niveles[35],pos_nivelesx,pos_nivelesy+sepy*3)
            b_lv37=boton(im.b_niveles[36],im.bo_niveles[36],pos_nivelesx+sepx,pos_nivelesy+sepy*3)
            b_lv38=boton(im.b_niveles[37],im.bo_niveles[37],pos_nivelesx+sepx*2,pos_nivelesy+sepy*3)
            b_lv39=boton(im.b_niveles[38],im.bo_niveles[38],pos_nivelesx+sepx*3,pos_nivelesy+sepy*3)
            b_lv40=boton(im.b_niveles[39],im.bo_niveles[39],pos_nivelesx+sepx*4,pos_nivelesy+sepy*3)
            
            
            if cursor.colliderect(b_lv21.rect) and click==True and avance[20]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[0]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv22.rect) and click==True and avance[21]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[1]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv23.rect) and click==True and avance[22]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[2]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv24.rect) and click==True and avance[23]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[3]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv25.rect) and click==True and avance[24]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[4]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv26.rect) and click==True and avance[25]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[5]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv27.rect) and click==True and avance[26]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[6]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv28.rect) and click==True and avance[27]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[7]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv29.rect) and click==True and avance[28]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[8]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv30.rect) and click==True and avance[29]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[9]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv31.rect) and click==True and avance[30]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[10]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv32.rect) and click==True and avance[31]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[11]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv33.rect) and click==True and avance[32]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[12]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv34.rect) and click==True and avance[33]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[13]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv35.rect) and click==True and avance[34]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[14]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv36.rect) and click==True and avance[35]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[15]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv37.rect) and click==True and avance[36]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[16]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv38.rect) and click==True and avance[37]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[17]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv39.rect) and click==True and avance[38]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[18]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv40.rect) and click==True and avance[39]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo2=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm2[19]=True
                LEFT=0.00001
                
            #actualizacion botones menu2
            b_lv21.update(pantalla, cursor)
            b_lv22.update(pantalla, cursor)
            b_lv23.update(pantalla, cursor)
            b_lv24.update(pantalla, cursor)
            b_lv25.update(pantalla, cursor)
            b_lv26.update(pantalla, cursor)
            b_lv27.update(pantalla, cursor)
            b_lv28.update(pantalla, cursor)
            b_lv29.update(pantalla, cursor)
            b_lv30.update(pantalla, cursor)
            b_lv31.update(pantalla, cursor)
            b_lv32.update(pantalla, cursor)
            b_lv33.update(pantalla, cursor)
            b_lv34.update(pantalla, cursor)
            b_lv35.update(pantalla, cursor)
            b_lv36.update(pantalla, cursor)
            b_lv37.update(pantalla, cursor)
            b_lv38.update(pantalla, cursor)
            b_lv39.update(pantalla, cursor)
            b_lv40.update(pantalla, cursor)
            
            
            av5=avance[20:25]
            av6=avance[25:30]
            av7=avance[30:35]
            av8=avance[35:40]
            for i in av5:
                for n in range(5):
                    if avance[n+20]==0:
                        pantalla.blit(im.bb_niveles[n+20],(pos_nivelesx+sepx*n,pos_nivelesy))
            for i in av6:
                for n in range(5):
                    if avance[n+25]==0:
                        pantalla.blit(im.bb_niveles[n+25],(pos_nivelesx+sepx*n,pos_nivelesy+sepy*1))
            for i in av7:
                for n in range(5):
                    if avance[n+30]==0:
                        pantalla.blit(im.bb_niveles[n+30],(pos_nivelesx+sepx*n,pos_nivelesy+sepy*2))
            for i in av8:
                for n in range(5):
                    if avance[n+35]==0:
                        pantalla.blit(im.bb_niveles[n+35],(pos_nivelesx+sepx*n,pos_nivelesy+sepy*3))

        """ #########################################################"""
        """ #########################################################"""
        """ ######################## MUNDO 3 ########################"""
        """ #########################################################"""    
        """ #########################################################"""
        if mundo3==True:
            UP,DOWN,RIGHT,LEFT="falso","falso","falso","falso"
            pmundo3=True
            
            if intro_old is None:
                pantalla1=pantalla.blit(im.fondo_mundo3,(pos_fondo,0))
                pantalla2=pantalla.blit(im.fondo_mundo3,(pos_fondo-1280,0))
            else:
                pantalla1=pantalla.blit(im.fondo_mundo3,intro_old,intro_old)
                pantalla2=pantalla.blit(im.fondo_mundo3,intro_old,intro_old)

            if pos_fondo>1280:
                pos_fondo=0
            pos_fondo=pos_fondo+vel_fondo

            
            
            #fondo dentro del juego 
            fondojuegox,fondojuegoy=-(fond/2)+1280/2,-(fond/2)+720/2
    
            #b_lv=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/blanco.png"),(int((2*ancho)/10),int(alto/2)))
            
            #POSICION INICIAL
            pos_b_mundosx,pos_b_mundosy=(ancho/10),(alto/4)
           
            """############# BOTONES NIVELES MUNDO 3 ############"""
            sepx=175
            sepy=125
            pos_nivelesx=ancho/5
            pos_nivelesy=alto/3
            b_lv41=boton(im.b_niveles[40],im.bo_niveles[40],pos_nivelesx,pos_nivelesy)
            b_lv42=boton(im.b_niveles[41],im.bo_niveles[41],pos_nivelesx+sepx,pos_nivelesy)
            b_lv43=boton(im.b_niveles[42],im.bo_niveles[42],pos_nivelesx+sepx*2,pos_nivelesy)
            b_lv44=boton(im.b_niveles[43],im.bo_niveles[43],pos_nivelesx+sepx*3,pos_nivelesy)
            b_lv45=boton(im.b_niveles[44],im.bo_niveles[44],pos_nivelesx+sepx*4,pos_nivelesy)
            b_lv46=boton(im.b_niveles[45],im.bo_niveles[45],pos_nivelesx,pos_nivelesy+sepy)
            b_lv47=boton(im.b_niveles[46],im.bo_niveles[46],pos_nivelesx+sepx,pos_nivelesy+sepy)
            b_lv48=boton(im.b_niveles[47],im.bo_niveles[47],pos_nivelesx+sepx*2,pos_nivelesy+sepy)
            b_lv49=boton(im.b_niveles[48],im.bo_niveles[48],pos_nivelesx+sepx*3,pos_nivelesy+sepy)
            b_lv50=boton(im.b_niveles[49],im.bo_niveles[49],pos_nivelesx+sepx*4,pos_nivelesy+sepy)
            
            
            if cursor.colliderect(b_lv41.rect) and click==True and avance[40]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo3=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm3[0]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv42.rect) and click==True and avance[41]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo3=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm3[1]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv43.rect) and click==True and avance[42]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo3=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm3[2]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv44.rect) and click==True and avance[43]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo3=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm3[3]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv45.rect) and click==True and avance[44]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo3=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm3[4]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv46.rect) and click==True and avance[45]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo3=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm3[5]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv47.rect) and click==True and avance[46]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo3=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm3[6]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv48.rect) and click==True and avance[47]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo3=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm3[7]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv49.rect) and click==True and avance[48]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo3=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm3[8]=True
                LEFT=0.00001
            if cursor.colliderect(b_lv50.rect) and click==True and avance[49]==1:
                pygame.mixer.Sound.play(s.click)
                click=False
                mundo3=False
                xinicial,yinicial=mousex,mousey
                juego=True
                nm3[9]=True
                LEFT=0.00001
            

            #actualizacion botones menu2
            b_lv41.update(pantalla, cursor)
            b_lv42.update(pantalla, cursor)
            b_lv43.update(pantalla, cursor)
            b_lv44.update(pantalla, cursor)
            b_lv45.update(pantalla, cursor)
            b_lv46.update(pantalla, cursor)
            b_lv47.update(pantalla, cursor)
            b_lv48.update(pantalla, cursor)
            b_lv49.update(pantalla, cursor)
            b_lv50.update(pantalla, cursor)
          
            
            av5=avance[40:45]
            av6=avance[45:50]

            for i in av5:
                for n in range(5):
                    if avance[n+40]==0:
                        pantalla.blit(im.bb_niveles[n+40],(pos_nivelesx+sepx*n,pos_nivelesy))
            for i in av6:
                for n in range(5):
                    if avance[n+45]==0:
                        pantalla.blit(im.bb_niveles[n+45],(pos_nivelesx+sepx*n,pos_nivelesy+sepy*1))
           

# m.centro=m.posicion-(COHETE.tamaño/2,COHETE.tamaño/2)
 #m.cohete=np.sqrt(((p2.centro[0])-(COHETE.posicion[0]))**2+((p2.centro[1])-(COHETE.posicion[1]))**2)
       #for m in planetas:             
        """######### condiciones para pasar de nivel #######"""
        
        nt=nm1+nm2+nm3
        lm1=l[0:19]
        lm2=l[20:39]
        lm3=l[40:50]
        try:
            for i in l: 
                if np.sqrt((((p2.posicion-(COHETE.tamaño/2,COHETE.tamaño/2))[0])-(COHETE.posicion[0]))**2+(((p2.posicion-(COHETE.tamaño/2,COHETE.tamaño/2))[1])-(COHETE.posicion[1]))**2)<p2.tamaño/2+COHETE.tamaño/2+.5 and i==True:
                    siguiente_nivel=True
                    siguiente2=True
                    juego=False
                    COHETE.posicion[0]=1000*100
                    COHETE.posicion[1]=-1000*100
                    if l[49]==True:
                        l[49]=False
                        juego=False
                        ganar=True
        except UnboundLocalError or ValueError or AttributeError: pass
            
        if siguiente_nivel==True and siguiente2==True:
            pantalla.blit(fondo_nivel,(fondojuegox, fondojuegoy))

            pygame.draw.rect(pantalla, c.darkslateblue, [400, 150, 500,450])
            
            texto("Por ahora",50,433+100,75+80+20,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("Sigues con vida",50,433+37,75+80+70,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            
            b_menu3=boton(im.b_menu,im.bo_menu,pospausax,pospausay+140-20)
            if cursor.colliderect(b_menu3.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                juego=False
                click=False
                pausa=False
                xinicial,yinicial=mousex,mousey
                siguiente2=False
                siguiente_nivel=False
                if pmundo1==True:
                    for m in nm1:
                        m=False
                    mundo1=True
                if pmundo2==True:
                    for m in nm2:
                        m=False
                    mundo2=True 
                if pmundo3==True:
                    for m in nm3:
                        m=False
                    mundo3=True 
            
            b_pausa2=boton(im.b_reiniciar,im.bo_reiniciar,pospausax,pospausay+70-20)
            if cursor.colliderect(b_pausa2.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                COHETE.posicion[0]=-10000
                juego=False
                click=False
                pausa=False
                xinicial,yinicial=mousex,mousey
                if True in l:
                    if 0<=l.index(True)<20:
                        nm1[l.index(True)]=True
                    elif 20<=l.index(True)<40:
                        nm2[l.index(True)-20]=True
                    elif 40<=l.index(True)<60:
                        nm3[l.index(True)-40]=True
                juego=True
                siguiente2=False
                siguiente_nivel=False
            
            b_siguiente=boton(im.b_siguiente,im.bo_siguiente,pospausax,pospausay-20)
            if cursor.colliderect(b_siguiente.rect) and click==True:
                siguiente2=False
                siguiente_nivel=False
                
                if l[19]==True:
                    nm2[0]=True
                    l[19]=False
                    pmundo1=False
                    pmundo2=True
                if l[39]==True:
                    nm3[0]=True
                    l[39]=False
                    pmundo2=False
                    pmundo3=True
                try:
                    for i in l: 
                        if i==True and i!=l[59]:
                            avance[l.index(True)+1]=1
                            siguiente=(l.index(i)+1)
                            if True in l:
                                l[l.index(True)]=False
                            if i in lm1:
                                nm1[siguiente]=True
                            elif i in lm2:
                                nm2[siguiente-20]=True
                            elif i in lm3:
                                if l[59]!=True:
                                    nm3[siguiente-40]=True         
                except UnboundLocalError or ValueError or AttributeError or IndexError: pass
                
                click=False
                xinicial,yinicial=mousex,mousey
                lost=False
                COHETE.posicion[0]=-100
                COHETE.posicion[1]=-100
                if True in l:
                    if 0<=l.index(True)<20:
                        nm1[l.index(True)]=True
                    elif 20<=l.index(True)<40:
                        nm2[l.index(True)-20]=True
                    elif 40<=l.index(True)<60:
                        nm3[l.index(True)-40]=True
            
            b_siguiente.update(pantalla, cursor)
            b_pausa2.update(pantalla, cursor)
            b_menu3.update(pantalla, cursor)
            
        """######################################################"""
        """######################################################"""
        """######################################################"""
        """######################################################"""
            
        if como_jugar==True:
            if intro_old is None:
                pantalla1=pantalla.blit(im.fondo_ganar,(pos_fondo,0))
                pantalla2=pantalla.blit(im.fondo_ganar,(pos_fondo-1280,0))
            else:
                pantalla1=pantalla.blit(im.fondo_ganar,intro_old,intro_old)
                pantalla2=pantalla.blit(im.fondo_ganar,intro_old,intro_old)
            if pos_fondo>1280:
                pos_fondo=0
            pos_fondo=pos_fondo+vel_fondo
            
            
            texto("OBJETIVO",60,ancho/2-125,150,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("Su objetivo es llevar un cohete con tripulantes a su",40,175,250,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("destino pasando por distintos sistemas planetarios",40,175,300,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("sin  dejarlos  morir. Para esto debe  tener en cuenta ",40,175,350,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("el  movimiento  orbital  de   los  planetas  y  algunas",40,175,400,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("                       limitaciones del cohete.",40,175,450,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
        
        if como_jugar2==True:
            if intro_old is None:
                pantalla1=pantalla.blit(im.fondo_ganar,(pos_fondo,0))
                pantalla2=pantalla.blit(im.fondo_ganar,(pos_fondo-1280,0))
            else:
                pantalla1=pantalla.blit(im.fondo_ganar,intro_old,intro_old)
                pantalla2=pantalla.blit(im.fondo_ganar,intro_old,intro_old)
            if pos_fondo>1280:
                pos_fondo=0
            pos_fondo=pos_fondo+vel_fondo
            
            
            
            texto("En tu viaje encontraras diversos objetos con los que podras",40,110,140,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("interactuar, por ejemplo:  ",40,110,190,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("Estrella",40,250,440,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("Planeta",40,550,440,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("Cohete",40,850,440,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            pantalla.blit(pygame.transform.scale(im.e2,(150,150)),(250,280))
            
            pantalla.blit(pygame.transform.scale(im.tutp2,(75,75)),(577.5,355))
            pantalla.blit(pygame.transform.scale(im.e4,(30,30)),(890,400))
        
        if como_jugar3==True:
            if intro_old is None:
                pantalla1=pantalla.blit(im.fondo_ganar,(pos_fondo,0))
                pantalla2=pantalla.blit(im.fondo_ganar,(pos_fondo-1280,0))
            else:
                pantalla1=pantalla.blit(im.fondo_ganar,intro_old,intro_old)
                pantalla2=pantalla.blit(im.fondo_ganar,intro_old,intro_old)
            if pos_fondo>1280:
                pos_fondo=0
            pos_fondo=pos_fondo+vel_fondo
            
           
            texto("Controles",60,ancho/2-125,150,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            
            pfx,pfy=180,380
            pantalla.blit(pygame.transform.rotate(im.flecha,180),(pfx,pfy))
            pantalla.blit(pygame.transform.rotate(im.flecha,90),(pfx+60,pfy-60))
            pantalla.blit(pygame.transform.rotate(im.flecha,270),(pfx+60,pfy))
            pantalla.blit(pygame.transform.rotate(im.flecha,0),(pfx+120,pfy))
            pantalla.blit(pygame.transform.rotate(im.b_r,0),(pfx+320,pfy-55))
            pantalla.blit(pygame.transform.rotate(im.b_p,0),(pfx+475,pfy-55))
            pantalla.blit(pygame.transform.rotate(im.b_esc,0),(pfx+630,pfy-55))
            pantalla.blit(pygame.transform.rotate(im.b_space,0),(pfx+785,pfy-70))
            texto("Izquierda",25,pfx-115,pfy+10,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("Derecha",25,pfx+175,pfy+10,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("Arriba",25,pfx+49,pfy-90,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("Abajo",25,pfx+54,pfy+50,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("Reiniciar",25,pfx+319,pfy-80,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("Pausa",25,pfx+494,pfy-80,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("Atras",25,pfx+649,pfy-80,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("Pantalla completa",25,pfx+772,pfy-80,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            
        if como_jugar==True or como_jugar2==True or como_jugar3==True or como_jugar4==True:
            b_adelante=boton(pygame.transform.rotate(im.b_atras,180),pygame.transform.rotate(im.bo_atras,180),pos_b_playx,pos_b_playy+225)                            
            b_adelante.update(pantalla, cursor)
            if cursor.colliderect(b_adelante.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                click=False
                if como_jugar==True:
                    como_jugar2=True
                    como_jugar=False
                elif como_jugar2==True:
                    como_jugar3=True
                    como_jugar2=False
                elif como_jugar3==True:
                    como_jugar4=True
                    como_jugar3=False
                elif como_jugar4==True:
                    como_jugar5=True
                    como_jugar4=False
            
        if como_jugar2==True or como_jugar3==True or como_jugar4==True:
            b_atras=boton(im.b_atras,im.bo_atras,pos_b_playx-500,pos_b_playy+225)                            
            b_atras.update(pantalla, cursor)
            if cursor.colliderect(b_atras.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                click=False
                if como_jugar2==True:
                    como_jugar=True
                    como_jugar2=False
                elif como_jugar3==True:
                    como_jugar2=True
                    como_jugar3=False
                elif como_jugar4==True:
                    como_jugar3=True
                    como_jugar4=False
                elif como_jugar5==True:
                    como_jugar4=True
                    como_jugar5=False

            #actualizacion botones menu
        """######################################################"""
        """######################################################"""
        """######################################################"""
        """######################################################"""
        
        if ganar==True:
            if intro_old is None:
                pantalla1=pantalla.blit(im.fondo_ganar,(pos_fondo,0))
                pantalla2=pantalla.blit(im.fondo_ganar,(pos_fondo-1280,0))
            else:
                pantalla1=pantalla.blit(im.fondo_ganar,intro_old,intro_old)
                pantalla2=pantalla.blit(im.fondo_ganar,intro_old,intro_old)
            if pos_fondo>1280:
                pos_fondo=0
            pos_fondo=pos_fondo+vel_fondo
            al=160
            texto("FIN",80,ancho/2-100,50+450,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("   ",60,ancho/2-125,50,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("Después  de  años  en  un  largo  viaje  alrededor",45,ancho/2-525+50,al,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("del universo los tripulantes que sobrevivieron",45,ancho/2-525+50,al+45,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("llegaron a su destino, pero  para su mala suerte",45,ancho/2-525+50,al+90,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("ya  no  habia  nadie,  todos  habian  muerto  hace",45,ancho/2-525+50,al+135,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("mucho tiempo en  una guerra nuclear. Al no tener ",45,ancho/2-525+50,al+180,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
            texto("nada, todos los viajeros restantes murieron.",45,ancho/2-525+50,al+225,c.white,"imagenes/fuentes/stalker/stalker1.ttf")
        """######################################################"""
        """######################################################"""
        """######################################################"""
        """######################################################"""
        cuadros=reloj.tick(30)
        cursor.update()
        Explosiones.update()
        Explosiones.draw(pantalla)
        pygame.display.update()
        
main()
