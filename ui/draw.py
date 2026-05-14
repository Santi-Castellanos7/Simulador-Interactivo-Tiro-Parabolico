import pygame

# DIBUJAR TEXTO EN LA PANTALLA
def draw_text(ventana, text, font, color, x, y):

    # Renderizar texto
    render = font.render(text, True, color)

    # Dibujar texto
    ventana.blit(render, (x, y))

# DIBUJAR LA TRAYECTORIA
def draw_trajectory(screen, trajectory, color):

    # Recorrer todos los puntos almacenados de la trayectoria
    for point in trajectory:
        pygame.draw.circle( screen, color,(int(point[0]), int(point[1])),4)

# DIBUJAR SUELO
def draw_ground(screen, color, width, ground_y):
    # Dibujar superficie del piso
    pygame.draw.rect(screen, color,(320, ground_y, width, 120))