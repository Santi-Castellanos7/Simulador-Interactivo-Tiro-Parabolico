import pygame

# =========================
# IMPORTAR MÓDULOS
# =========================
from config import constants
from physics.fisicas import (
    calcular_escala,
    calcular_velocidad,
    calcular_posicion
)
from ui.draw import (
    draw_text,
    draw_trajectory,
    draw_ground
)

# =========================
# INICIALIZAR PYGAME
# =========================
pygame.init()

screen = pygame.display.set_mode((constants.ANCHO_VENTANA, constants.ALTO_VENTANA))
pygame.display.set_caption("Simulador de Tiro Parabólico - UPTC")
clock = pygame.time.Clock()

# =========================
# FUENTES
# =========================
title_font = pygame.font.SysFont("Arial", 30, bold=True)
info_font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 18)

# =========================
# VARIABLES DE ESTADO
# =========================
velocidad_inicial = constants.VELOCIDAD_INICIAL
angulo = constants.ANGULO
escala = constants.ESCALA_INICIAL
tiempo = 0
lanzamiento_activo = False

# Variables de velocidad actual para la interfaz
v_x_actual = 0
v_y_actual = 0

proyectil_x = constants.INICIAL_X
proyectil_y = constants.INICIAL_Y

trayectoria = []
altura_maxima = 0
alcance_maximo = 0

punto_altura_maxima = None
punto_alcance = None

# =========================
# BUCLE PRINCIPAL
# =========================
running = True
while running:

    dt = clock.tick(constants.FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lanzamiento_activo = True
                tiempo = 0
                trayectoria.clear()
                altura_maxima = 0
                alcance_maximo = 0
                punto_altura_maxima = None
                punto_alcance = None

                escala = calcular_escala(
                    constants.ANCHO_VENTANA, constants.ALTO_VENTANA,
                    constants.INICIAL_X, constants.INICIAL_Y,
                    velocidad_inicial, angulo, constants.GRAVEDAD
                )

            if event.key == pygame.K_r:
                lanzamiento_activo = False
                tiempo = 0
                proyectil_x = constants.INICIAL_X
                proyectil_y = constants.INICIAL_Y
                trayectoria.clear()
                punto_altura_maxima = None
                punto_alcance = None

            if event.key == pygame.K_UP: velocidad_inicial += 2
            if event.key == pygame.K_DOWN: velocidad_inicial -= 2
            if event.key == pygame.K_RIGHT: angulo += 2
            if event.key == pygame.K_LEFT: angulo -= 2

    # Cálculos cinemáticos base
    velocidad_inicial = max(5, min(velocidad_inicial, 100))
    angulo = max(5, min(angulo, 85))
    v_x_inicial, v_y_inicial = calcular_velocidad(velocidad_inicial, angulo)

    # =========================
    # LÓGICA DE MOVIMIENTO
    # =========================
    if lanzamiento_activo:
        tiempo += dt * 2
        proyectil_x, proyectil_y = calcular_posicion(
            constants.INICIAL_X, constants.INICIAL_Y,
            v_x_inicial, v_y_inicial, constants.GRAVEDAD, tiempo, escala
        )

        # Actualizamos velocidades mientras vuela
        v_x_actual = v_x_inicial
        v_y_actual = v_y_inicial - (constants.GRAVEDAD * tiempo)

        if proyectil_y <= constants.INICIAL_Y:
            trayectoria.append((proyectil_x, proyectil_y))

            # Altura máxima
            alt_actual = (constants.INICIAL_Y - proyectil_y) / escala
            if alt_actual > altura_maxima:
                altura_maxima = alt_actual
                punto_altura_maxima = (proyectil_x, proyectil_y)

            alcance_maximo = (proyectil_x - constants.INICIAL_X) / escala
        else:
            # IMPACTO: Forzamos todo a cero
            punto_alcance = (proyectil_x, constants.INICIAL_Y)
            proyectil_y = constants.INICIAL_Y
            v_x_actual = 0
            v_y_actual = 0
            lanzamiento_activo = False
    else:
        # Reposo o ajuste de parámetros
        v_x_actual = 0
        v_y_actual = 0

    # =========================
    # RENDERIZADO (DIBUJO)
    # =========================
    screen.fill(constants.AZUL_CIELO)
    draw_ground(screen, constants.VERDE_PASTO, constants.ANCHO_VENTANA, constants.INICIAL_Y)

    # PANEL LATERAL
    pygame.draw.rect(screen, constants.PANEL_LATERAL, (0, 0, 320, constants.ALTO_VENTANA))
    draw_text(screen, "SIMULADOR FÍSICA", title_font, constants.CYAN, 20, 20)

    # RECUADRO DE DATOS
    pygame.draw.rect(screen, constants.PANEL_INTERNO, (15, 70, 290, 320), border_radius=12)
    pygame.draw.rect(screen, constants.BORDES, (15, 70, 290, 320), 2, border_radius=12)

    textos_datos = [
        f"V. Inicial: {velocidad_inicial} m/s",
        f"Ángulo: {angulo}°",
        f"Vel X Actual: {round(v_x_actual, 2)} m/s",
        f"Vel Y Actual: {round(v_y_actual, 2)} m/s",
        f"Tiempo: {round(tiempo, 2)} s",
        f"Alt. Máx: {round(altura_maxima, 2)} m",
        f"Alcance: {round(alcance_maximo, 2)} m"
    ]
    for i, t in enumerate(textos_datos):
        draw_text(screen, t, info_font, constants.BLANCO, 30, 85 + (i * 38))

    # RECUADRO DE CONTROLES
    pygame.draw.rect(screen, constants.PANEL_INTERNO, (15, 410, 290, 160), border_radius=12)
    pygame.draw.rect(screen, constants.BORDES, (15, 410, 290, 160), 2, border_radius=12)

    draw_text(screen, "CONTROLES", info_font, constants.CYAN, 30, 425)
    controles = [
        "[ESPACIO] Lanzar Proyectil",
        "[R] Reiniciar Simulación",
        "[↑ / ↓] Ajustar Velocidad",
        "[← / →] Ajustar Ángulo"
    ]
    for i, inst in enumerate(controles):
        draw_text(screen, inst, small_font, constants.BLANCO, 30, 465 + (i * 22))

    # DIBUJAR TRAYECTORIA Y PROYECTIL
    draw_trajectory(screen, trayectoria, constants.AMARILLO)

    if punto_altura_maxima:
        pygame.draw.circle(screen, constants.VERDE, (int(punto_altura_maxima[0]), int(punto_altura_maxima[1])), 6)
        draw_text(screen, f"Altura máxima: {round(altura_maxima, 1)}m", small_font, constants.NEGRO,
                  punto_altura_maxima[0] - 15, punto_altura_maxima[1] - 25)

    if punto_alcance:
        pygame.draw.circle(screen, constants.NARANJA, (int(punto_alcance[0]), int(punto_alcance[1])), 10)
        draw_text(screen, f"Alcance máxima: {round(alcance_maximo, 1)}m", small_font, constants.NEGRO,
                  punto_alcance[0] - 40, punto_alcance[1] + 15)

    pygame.draw.circle(screen, constants.ROJO, (int(proyectil_x), int(proyectil_y)), 14)

    pygame.display.update()

pygame.quit()