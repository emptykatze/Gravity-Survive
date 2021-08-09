import pygame, sys
import numpy as np
from imagenes import imagenes  as im

"""
Definir clase planeta ////////////////////////////////////////////////////////////////7
"""
class planeta:
    def __init__(self, masa, posicion, velocidad): #posicion y velocidad = vectores de R2
        self.masa = masa
        self.posicion = np.array(posicion)
        self.momentum = masa * np.array(velocidad)

    #Calcular fuerza sobre self por p2 (Ley de gravitacion universal)
    def fuerzag(self, p2):
        G = 0.8 #valor real=0.000000000066738
        r_vec = self.posicion - p2.posicion
        r_mag = np.linalg.norm(r_vec)
        r_unit = r_vec / r_mag
        fuerza_mag = G * self.masa * p2.masa / r_mag ** 2
        fuerza_vec = -fuerza_mag * r_unit
        return fuerza_vec
"""
Parametros del Juego /////////////////////////////////////////////////////////////////////////////////////
"""
pygame.init()
reloj = pygame.time.Clock()
pygame.display.set_caption("Juego sistema solar")
size = 1200, 700
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)

#Cargar imagenes de los planetas
p1_imagen = pygame.transform.scale(pygame.image.load("imagenes/intro/planeta1.png"),(25,25))
p2_imagen = pygame.image.load("imagenes/intro/sol.png")

#Asignar los atributos de los planetas
p1 = planeta(500, [600, 80], [40, 0])
p2 = planeta(500000, [600, 350], [0, 0])
p3 = planeta(50, [300, 200], [5, 20])
p4 = planeta(50, [600, 20], [30,5])
#lista con los planetas
planetas = [p1,p2,p3,p4]


#Parametros de tiempo
dt = 0.1
t = 0
"""
Ciclo de juego/////////////////////////////////////////////////////////////////////////////////
"""

while True:
    while t <= 1000:
        
        
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

        # Actualizar posiciones
        for m in planetas:
            m.posicion = m.posicion + m.momentum / m.masa * dt

        #Iniciar cada frame completamente negro
        screen.fill((0,0,0))
        screen.blit(im.fondo1, (0, 0))
        #Colocar la imagen de cada planeta en pantalla
        screen.blit(p1_imagen, p1.posicion)
        screen.blit(p2_imagen,p2.posicion)
        screen.blit(p1_imagen, p3.posicion)
        screen.blit(p1_imagen, p4.posicion)
        #actualizar pantalla
        pygame.display.update()
        #actualizar el tiempo transcurrido
        t = t + dt

        #Salir del juego al hacer click en el boton cerrar aplicacion
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #Tasa de refresco (fps)
        a=reloj.tick(50)
        print(a)

