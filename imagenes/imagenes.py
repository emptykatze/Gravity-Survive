# -*- coding: utf-8 -*-
"""
imagenes del juego
"""
import pygame
pygame.init()

#icono
icono=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/b_atras.png"),(200,200))
sound=pygame.transform.scale(pygame.image.load("imagenes/iconos/sound.png"),(35,35))
music=pygame.transform.scale(pygame.image.load("imagenes/iconos/music.png"),(35,35))

ancho,alto=1280,720
#tamaño de los botones del menu
b_ancho,b_alto=int(452/2),int(200/4)

# Menú

#fondos
fondo1=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/negro.png"),(12800^2,12800^2))
fondo2=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/negro.png"),(1280,720))

"""fondo_mundo1=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/negro.png"),(12800^2,12800^2))
fondo_mundo2=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/negro.png"),(12800^2,12800^2))
fondo_mundo3=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/negro.png"),(12800^2,12800^2))
fondo_ganar=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/negro.png"),(12800^2,12800^2))
"""

fondo_mundo1=pygame.transform.scale(pygame.image.load("imagenes/fondos/am.png"),(1280,720))
fondo_mundo2=pygame.transform.scale(pygame.image.load("imagenes/fondos/v.png"),(1280,720))
fondo_mundo3=pygame.transform.scale(pygame.image.load("imagenes/fondos/r.png"),(1280,720))
fondo_ganar=pygame.transform.scale(pygame.image.load("imagenes/fondos/a.png"),(1280,720))

#jugar
b_jugar=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/b_jugar.png"),(b_ancho,b_alto))
bo_jugar=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/bo_jugar.png"),(b_ancho,b_alto))
#salir
b_salir=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/b_salir.png"),(b_ancho,b_alto))
bo_salir=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/bo_salir.png"),(b_ancho,b_alto))
#opciones
b_opciones=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/b_opciones.png"),(b_ancho,b_alto))
bo_opciones=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/bo_opciones.png"),(b_ancho,b_alto))
#como jugar
b_como_jugar=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/b_como_jugar.png"),(b_ancho,b_alto))
bo_como_jugar=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/bo_como_jugar.png"),(b_ancho,b_alto))

#atras
b_atras=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/b_atras.png"),(int(b_alto),int(b_alto)))
bo_atras=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/bo_atras.png"),(int(b_alto/2*1.5),int(b_alto/2*1.5)))

#Boton deslizable
des1=pygame.image.load("imagenes/menu_principal/des1.png")
des2=pygame.image.load("imagenes/menu_principal/des2.png")


negro=pygame.transform.scale(pygame.image.load("negro.jpg"),(1280,720))

#botones de mundos
b_mundo1=pygame.transform.scale(pygame.image.load("imagenes/mundos/b_mundo1.png"),(int((2*ancho)/10),int(alto/2)))
bo_mundo1=pygame.transform.scale(pygame.image.load("imagenes/mundos/bo_mundo1.png"),(int((2*ancho)/10),int(alto/2)))
b_mundo2=pygame.transform.scale(pygame.image.load("imagenes/mundos/b_mundo2.png"),(int((2*ancho)/10),int(alto/2)))
bo_mundo2=pygame.transform.scale(pygame.image.load("imagenes/mundos/bo_mundo2.png"),(int((2*ancho)/10),int(alto/2)))
b_mundo3=pygame.transform.scale(pygame.image.load("imagenes/mundos/b_mundo3.png"),(int((2*ancho)/10),int(alto/2)))
bo_mundo3=pygame.transform.scale(pygame.image.load("imagenes/mundos/bo_mundo3.png"),(int((2*ancho)/10),int(alto/2)))

#boton pausa
b_menu=pygame.transform.scale(pygame.image.load("imagenes/pausa/b_menu.png"),(int((2*ancho)/9),int(alto/14)))
bo_menu=pygame.transform.scale(pygame.image.load("imagenes/pausa/bo_menu.png"),(int((2*ancho)/9),int(alto/14)))
b_reanudar=pygame.transform.scale(pygame.image.load("imagenes/pausa/b_reanudar.png"),(int((2*ancho)/9),int(alto/14)))
bo_reanudar=pygame.transform.scale(pygame.image.load("imagenes/pausa/bo_reanudar.png"),(int((2*ancho)/9),int(alto/14)))
b_reiniciar=pygame.transform.scale(pygame.image.load("imagenes/pausa/b_reiniciar.png"),(int((2*ancho)/9),int(alto/14)))
bo_reiniciar=pygame.transform.scale(pygame.image.load("imagenes/pausa/bo_reiniciar.png"),(int((2*ancho)/9),int(alto/14)))

#siguiente
b_siguiente=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/b_siguiente.png"),(int((2*ancho)/9),int(alto/14)))
bo_siguiente=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/bo_siguiente.png"),(int((2*ancho)/9),int(alto/14)))
                                    
#boton niveles
b_lv1=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/blanco.png"),(int((2*ancho)/30),int(alto/10)))
bo_lv1=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/morado.png"),(int((2*ancho)/30),int(alto/10)))

"""planetas"""
plt=2
if plt==1:
    p1=pygame.transform.scale(pygame.image.load("imagenes/Planetas/p4.png"),(50,50))
    p2=pygame.transform.scale(pygame.image.load("imagenes/Planetas/p5.png"),(50,50))
    p3=pygame.transform.scale(pygame.image.load("imagenes/Planetas/p6.png"),(50,50))
    p4=pygame.transform.scale(pygame.image.load("imagenes/Planetas/p4.png"),(50,50))
    p5=pygame.transform.scale(pygame.image.load("imagenes/Planetas/p5.png"),(50,50))
    p6=pygame.transform.scale(pygame.image.load("imagenes/Planetas/p6.png"),(50,50))
    p7=pygame.transform.scale(pygame.image.load("imagenes/Planetas/p7.png"),(50,50))
if plt!=1:
    p0=pygame.transform.scale(pygame.image.load("imagenes/planets/0.png"),(50,50))
    p1=pygame.transform.scale(pygame.image.load("imagenes/planets/1.png"),(50,50))
    p2=pygame.transform.scale(pygame.image.load("imagenes/planets/2.png"),(50,50))
    p3=pygame.transform.scale(pygame.image.load("imagenes/planets/3.png"),(50,50))
    p4=pygame.transform.scale(pygame.image.load("imagenes/planets/4.png"),(50,50))
    p5=pygame.transform.scale(pygame.image.load("imagenes/planets/5.png"),(50,50))
    p6=pygame.transform.scale(pygame.image.load("imagenes/planets/6.png"),(50,50))
    p7=pygame.transform.scale(pygame.image.load("imagenes/planets/7.png"),(50,50))
    p8=pygame.transform.scale(pygame.image.load("imagenes/planets/8.png"),(50,50))
    p9=pygame.transform.scale(pygame.image.load("imagenes/planets/9.png"),(50,50))
    p10=pygame.transform.scale(pygame.image.load("imagenes/planets/10.png"),(50,50))
    p11=pygame.transform.scale(pygame.image.load("imagenes/planets/11.png"),(50,50))
    p12=pygame.transform.scale(pygame.image.load("imagenes/planets/12.png"),(50,50))
    p13=pygame.transform.scale(pygame.image.load("imagenes/planets/13.png"),(50,50))
    p14=pygame.transform.scale(pygame.image.load("imagenes/planets/14.png"),(50,50))
    p15=pygame.transform.scale(pygame.image.load("imagenes/planets/15.png"),(50,50))
    p16=pygame.transform.scale(pygame.image.load("imagenes/planets/16.png"),(50,50))
    p17=pygame.transform.scale(pygame.image.load("imagenes/planets/17.png"),(50,50))
    p18=pygame.transform.scale(pygame.image.load("imagenes/planets/18.png"),(50,50))
    p19=pygame.transform.scale(pygame.image.load("imagenes/planets/19.png"),(50,50))
    p20=pygame.transform.scale(pygame.image.load("imagenes/planets/20.png"),(50,50))
    p21=pygame.transform.scale(pygame.image.load("imagenes/planets/21.png"),(50,50))
    p22=pygame.transform.scale(pygame.image.load("imagenes/planets/22.png"),(50,50))
    p23=pygame.transform.scale(pygame.image.load("imagenes/planets/23.png"),(50,50))
    p24=pygame.transform.scale(pygame.image.load("imagenes/planets/24.png"),(50,50))
    
tutp2=pygame.image.load("imagenes/planets/2.png")
"""estrellas"""
if plt==1:
    e1=pygame.transform.scale(pygame.image.load("imagenes/Planetas/e1.png"),(100,100))
    e2=pygame.transform.scale(pygame.image.load("imagenes/Planetas/e2.png"),(150,150))
    e3=pygame.transform.scale(pygame.image.load("imagenes/Planetas/e3.png"),(200,200))
    e4=pygame.transform.scale(pygame.image.load("imagenes/Planetas/e4.png"),(200,200))
if plt!=1:
    e1=pygame.image.load("imagenes/planets/e1.png")
    e2=pygame.image.load("imagenes/planets/e2.png")
    e3=pygame.image.load("imagenes/planets/e3.png")
    e4=pygame.image.load("imagenes/planets/e4.png")

"""niveles"""
b_niveles=[]
for x in range(60):
    niveles=f'{x+1}.png'
    imagen=pygame.image.load(f'imagenes/niveles/{niveles}')
    imagen=pygame.transform.scale(imagen,(int((2*ancho)/30),int(alto/10)))
    b_niveles=b_niveles+[imagen]
"""niveles 2"""
bo_niveles=[]
for x in range(60):
    niveles=f'{x+1}.png'
    imagen=pygame.image.load(f'imagenes/niveles2/{niveles}')
    imagen=pygame.transform.scale(imagen,(int((2*ancho)/30),int(alto/10)))
    bo_niveles=bo_niveles+[imagen]
"""niveles 3"""
bb_niveles=[]
for x in range(60):
    niveles=f'{x+1}.png'
    imagen=pygame.image.load(f'imagenes/niveles3/{niveles}')
    imagen=pygame.transform.scale(imagen,(int((2*ancho)/30),int(alto/10)))
    bb_niveles=bb_niveles+[imagen]
    
"""Teclas"""
flecha=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/flecha.png"),(50,50))
b_r=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/r.png"),(100,100))
b_p=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/p.png"),(100,100))
b_esc=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/esc.png"),(100,100))
b_space=pygame.transform.scale(pygame.image.load("imagenes/menu_principal/space.png"),(170,130))
            

""" explosiones """
animacion_explosion={'t1':[],'t2':[],'t3':[],'t4':[]}
for x in range(24):
    archivo_explosiones=f'expl_01_{x:04d}.png'
    imagenes=pygame.image.load(f'imagenes/explosiones/1/{archivo_explosiones}')
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
        pygame.sprite.Sprite.__init_(self)
        self.dimensiones=dimensiones
        self.image=animacion_explosion[self.dimensiones][0]
        self.rect=self.image.get_rect()
        self.rect.center=centro
        self.fotograma=0
        self.frecuencia_fotograma=35
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
                        
        
             