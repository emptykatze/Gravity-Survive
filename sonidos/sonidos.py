# -*- coding: utf-8 -*-
"""
Musica y efectos de sonido
"""
import pygame
pygame.mixer.init()

#musica_menu=pygame.mixer.Sound("sonidos/principal/TheySay-menu.mp3")
#https://www.fiftysounds.com/es/musica-libre-de-derechos/dicen.html
musica_menu_3=pygame.mixer.Sound("sonidos/principal/POL-the-challenge-short.wav")
"Background music from PlayOnLoop.com Licensed under Creative Commons by Attribution 4.0"

click=pygame.mixer.Sound("sonidos/efectos/cli.wav")
loose=pygame.mixer.Sound("sonidos/efectos/loose.wav")
win=pygame.mixer.Sound("sonidos/efectos/win.wav")
