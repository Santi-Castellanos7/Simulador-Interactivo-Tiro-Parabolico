import pygame

def draw_text(ventana, text, font, color, x, y):
    render = font.render(text, True, color)
    ventana.blit(render, (x, y))

def draw_trajectory(screen, trajectory, color):
    # Dibujamos círculos pequeños para la trayectoria
    for point in trajectory:
        pygame.draw.circle(screen, color, (int(point[0]), int(point[1])), 4)

def draw_ground(screen, color, width, ground_y):
    # El suelo ahora se dibuja desde el panel lateral hacia la derecha
    pygame.draw.rect(screen, color, (320, ground_y, width, 120))