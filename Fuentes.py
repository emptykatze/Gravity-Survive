# -*- coding: utf-8 -*-



"""
Juego sistema planetario
"""
import pygame,sys,time
from pygame.locals import*
from librerias import Colores as c
from imagenes import imagenes  as im
from sonidos import sonidos as s
from copy import copy


#tamaño de pantalla
ancho,alto=1280,720
pantalla = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)

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
    pantalla.blit(tex,(x,y))

cursor=cursor()
reloj=pygame.time.Clock()


# FUNCIÓN PRINCIPAL
def main():
    pygame.init()   
    pygame.mixer.init()
    pygame.display.set_caption('Juego')
    
    #SONIDOS
    vol=0.5
    sound=0.5
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.Sound.set_volume(s.click,sound)
    sclick=pygame.mixer.Sound.play(s.click)
      
    #Pantallas del juego
    menu=True
    juego=False
    opciones=False
    pausa=False
    
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

    # LOOP PRINCIPAL
    while True:
        
        if click2==True:
            click_sostenido=False
        click2=False
        click=False
        
            
        #Eventos de mouse y teclado
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    if menu==True:
                        pygame.quit()
                        sys.exit()
                    if menu==False:
                        menu=True
                        juego=False
                        opciones=False
            elif event.type==MOUSEMOTION:
                mousex,mousey=event.pos
            elif event.type==MOUSEBUTTONDOWN:
               click=True
               click_sostenido=True
               mousex,mousey=event.pos  
               mousesx,mousesy=event.pos
            elif event.type==MOUSEBUTTONUP :
                mousex,mousey=event.pos
                click2=True
              
                
        
        
        #menu
        if menu==True:
            pantalla.blit(im.negro,(0,0))                        
            color=c.green
            #boton de jugar
            pos_b_playx,pos_b_playy=0,0
            b_play=boton(im.b_atras,im.bo_atras,pos_b_playx,pos_b_playy)
            if cursor.colliderect(b_play.rect) and click==True:
                pygame.mixer.Sound.play(s.click)
                menu=False
                juego=True
            
            #texto("En construcción", 50,325,30, color, "imagenes/fuentes/cat-faces/CatFaces.otf")
            #texto("En construcción", 50,325,90, color,"imagenes/fuentes/graystroke/GRAYSTROKE_ITALIC.otf")
            #texto("En construcción", 50,325,150, color,"imagenes/fuentes/graystroke/GRAYSTROKE_REGULAR.otf")
            #texto("En construcción", 50,325,210, color,"imagenes/fuentes/groteskia/GROTESKIA_OBLIQUE.otf")
            #texto("Jugar    Pausa    Opciones    Salir ", 50,200,30, color, "imagenes/fuentes/groteskia/GROTESKIA.otf")
            #texto("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z", 50,200,90, color,  "imagenes/fuentes/groteskia/GROTESKIA.otf")
            #texto("a b c d e f g h i j k l m n o p q r s t u v w x y z", 50,200,150, color, "imagenes/fuentes/groteskia/GROTESKIA.otf")
            #texto("1 2 3 4 5 6 7 8 9 0 ! ? , . á é í ó ú", 50,200,210, color, "imagenes/fuentes/groteskia/GROTESKIA.otf")
            
            texto("Jugar    Pausa    Opciones    Salir", 50,200,300, color, "imagenes/fuentes/stalker/stalker1.ttf")
            texto("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z", 50,200,360, color,  "imagenes/fuentes/stalker/stalker1.ttf")
            texto("a b c d e f g h i j k l m n o p q r s t u v w x y z", 50,200,420, color, "imagenes/fuentes/stalker/stalker1.ttf")
            texto(" , . á é í ó ú ( ) [ ] { } = + - * \'  / % $ & # \"", 50,200,480, color, "imagenes/fuentes/stalker/stalker1.ttf")
            
        #actualizacion botones menu
        b_play.update(pantalla, cursor)
       
        #JUEGO
        if juego==True:
            pantalla.blit(im.negro,(0,0))
            
            texto("En construcción", 50,325,30, color, "imagenes/fuentes/tricks/Tricks.ttf")
            texto("En construcción", 50,325,90, color,"imagenes/fuentes/tricks/TricksHollow.ttf")
            texto("En construcción", 50,325,150, color,"imagenes/fuentes/tricks/TricksHollow-Italic.ttf")
            texto("En construcción", 50,325,210, color,"imagenes/fuentes/tricks/Tricks-Italic.ttf")
            texto("En construcción", 50,325,270, color, "imagenes/fuentes/wanderlust-typewriter/WanderlustTypewriterDemo-Regular.ttf")
            texto("En construcción", 50,325,330, color, "imagenes/fuentes/xayax/XAyax.ttf")
            texto("En construcción", 50,325,390, color, "imagenes/fuentes/xayax/XAyax_O.ttf")
            texto("En construcción", 50,325,450, color, "imagenes/fuentes/xayax/XAyax_S.ttf")
            #texto("En construcción", 50,325,510, c.yellow, "imagenes/fuentes/stalker/stalker1.ttf")
            #texto("En construcción", 50,325,570, c.yellow, "imagenes/fuentes/stalker/stalker2.ttf")
            #texto("En construcción", 50,325,630, c.yellow, "imagenes/fuentes/times_new_roman/times.ttf")
            
        
        
        
        #Pausa
        if pausa==True:
            pantalla.blit(im.fondo,(0,0))
            

        reloj.tick(60)
        cursor.update()
        pygame.display.update()

main()