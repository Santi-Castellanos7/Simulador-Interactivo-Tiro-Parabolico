import pygame

from config import constants

#Inicializar la libreria de pygame
pygame.init()

#Crear ventana del juego

ventana = pygame.display.set_mode(constants.ALTO_VENTANA, constants.ANCHO_VENTANA)

#Ponerle nombre a la ventana

pygame.display.set_caption("Simulador interactivo de tiro parabólico")


running = True
clock = pygame.time.Clock()

#
while running:

    clock.tick(constants.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False







