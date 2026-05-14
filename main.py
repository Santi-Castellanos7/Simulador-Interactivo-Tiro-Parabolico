import pygame

# =========================
# IMPORTAR CONSTANTES
# =========================
from config.constants import *

# =========================
# IMPORTAR FÍSICA
# =========================
from physics.fisicas import (
    calcular_escala,
    calcular_velocidad,
    calcular_posicion
)

# =========================
# IMPORTAR INTERFAZ
# =========================
from ui.draw import (
    draw_text,
    draw_trajectory,
    draw_ground
)

# =========================
# INICIALIZAR PYGAME
# =========================
pygame.init()

# =========================
# CREAR VENTANA
# =========================
screen = pygame.display.set_mode(
    (
        ANCHO_VENTANA,
        ALTO_VENTANA
    )
)

pygame.display.set_caption(
    "Simulador de Tiro Parabólico"
)

clock = pygame.time.Clock()

# =========================
# FUENTES
# =========================
title_font = pygame.font.SysFont(
    "Arial",
    34,
    bold=True
)

info_font = pygame.font.SysFont(
    "Arial",
    24
)

small_font = pygame.font.SysFont(
    "Arial",
    20
)

# =========================
# VARIABLES DEL PROYECTIL
# =========================
velocidad_inicial = VELOCIDAD_INICIAL

angulo = ANGULO

escala = ESCALA_INICIAL

# =========================
# VARIABLES DE SIMULACIÓN
# =========================
tiempo = TIEMPO

lanzamiento_activo = LANZADOR

proyectil_x = INICIAL_X
proyectil_y = INICIAL_Y

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

    # Controlar FPS
    clock.tick(FPS)

    # =========================
    # EVENTOS
    # =========================
    for event in pygame.event.get():

        # Cerrar ventana
        if event.type == pygame.QUIT:
            running = False

        # Eventos del teclado
        if event.type == pygame.KEYDOWN:

            # =========================
            # INICIAR LANZAMIENTO
            # =========================
            if event.key == pygame.K_SPACE:

                lanzamiento_activo = True

                tiempo = 0

                trayectoria.clear()

                altura_maxima = 0
                alcance_maximo = 0

                punto_altura_maxima = None
                punto_alcance = None

                # Calcular escala dinámica
                escala = calcular_escala(
                    ANCHO_VENTANA,
                    ALTO_VENTANA,
                    INICIAL_X,
                    INICIAL_Y,
                    velocidad_inicial,
                    angulo,
                    GRAVEDAD
                )

            # =========================
            # REINICIAR SIMULACIÓN
            # =========================
            if event.key == pygame.K_r:

                lanzamiento_activo = False

                tiempo = 0

                proyectil_x = INICIAL_X
                proyectil_y = INICIAL_Y

                trayectoria.clear()

            # =========================
            # MODIFICAR VELOCIDAD
            # =========================
            if event.key == pygame.K_UP:
                velocidad_inicial += 2

            if event.key == pygame.K_DOWN:
                velocidad_inicial -= 2

            # =========================
            # MODIFICAR ÁNGULO
            # =========================
            if event.key == pygame.K_RIGHT:
                angulo += 2

            if event.key == pygame.K_LEFT:
                angulo -= 2

    # =========================
    # VALIDACIONES
    # =========================
    velocidad_inicial = max(
        5,
        min(velocidad_inicial, 100)
    )

    angulo = max(
        5,
        min(angulo, 85)
    )

    # =========================
    # CALCULAR VELOCIDADES
    # =========================
    velocidad_x, velocidad_y = calcular_velocidad(
        velocidad_inicial,
        angulo
    )

    # =========================
    # FONDO
    # =========================
    screen.fill(AZUL_CIELO)

    # =========================
    # PANEL LATERAL
    # =========================
    pygame.draw.rect(
        screen,
        PANEL_LATERAL,
        (0, 0, 320, ALTO_VENTANA),
        border_radius=15
    )

    # =========================
    # TARJETA INFORMACIÓN
    # =========================
    pygame.draw.rect(
        screen,
        PANEL_INTERNO,
        (15, 80, 290, 340),
        border_radius=15
    )

    pygame.draw.rect(
        screen,
        BORDES,
        (15, 80, 290, 340),
        3,
        border_radius=15
    )

    # =========================
    # TARJETA CONTROLES
    # =========================
    pygame.draw.rect(
        screen,
        PANEL_INTERNO,
        (15, 450, 290, 180),
        border_radius=15
    )

    pygame.draw.rect(
        screen,
        BORDES,
        (15, 450, 290, 180),
        3,
        border_radius=15
    )

    # =========================
    # TÍTULO
    # =========================
    draw_text(
        screen,
        "SIMULADOR FÍSICA",
        title_font,
        CYAN,
        20,
        20
    )

    # =========================
    # INFORMACIÓN
    # =========================
    draw_text(
        screen,
        f"Velocidad Inicial: {velocidad_inicial} m/s",
        info_font,
        BLANCO,
        30,
        100
    )

    draw_text(
        screen,
        f"Ángulo: {angulo}°",
        info_font,
        BLANCO,
        30,
        140
    )

    draw_text(
        screen,
        f"Tiempo: {round(tiempo, 2)} s",
        info_font,
        BLANCO,
        30,
        180
    )

    draw_text(
        screen,
        f"Velocidad X: {round(velocidad_x, 2)}",
        info_font,
        BLANCO,
        30,
        220
    )

    draw_text(
        screen,
        f"Velocidad Y: {round(velocidad_y, 2)}",
        info_font,
        BLANCO,
        30,
        260
    )

    draw_text(
        screen,
        f"Altura Máxima: {round(altura_maxima, 2)} m",
        info_font,
        BLANCO,
        30,
        300
    )

    draw_text(
        screen,
        f"Alcance Máximo: {round(alcance_maximo, 2)} m",
        info_font,
        BLANCO,
        30,
        340
    )

    # =========================
    # CONTROLES
    # =========================
    draw_text(
        screen,
        "CONTROLES",
        info_font,
        CYAN,
        30,
        470
    )

    controles = [
        "ESPACIO = Lanzar",
        "R = Reiniciar",
        "↑ ↓ = Velocidad",
        "← → = Ángulo"
    ]

    for i, control in enumerate(controles):

        draw_text(
            screen,
            control,
            small_font,
            BLANCO,
            30,
            520 + (i * 30)
        )

    # =========================
    # DIBUJAR PISO
    # =========================
    draw_ground(
        screen,
        VERDE_PASTO,
        ANCHO_VENTANA,
        INICIAL_Y
    )

    # =========================
    # MOVIMIENTO
    # =========================
    if lanzamiento_activo:

        # Actualizar tiempo
        tiempo += 0.05

        # Calcular posición
        proyectil_x, proyectil_y = calcular_posicion(
            INICIAL_X,
            INICIAL_Y,
            velocidad_x,
            velocidad_y,
            GRAVEDAD,
            tiempo,
            escala
        )

        # Guardar trayectoria
        trayectoria.append(
            (
                proyectil_x,
                proyectil_y
            )
        )

        # Calcular altura máxima
        altura_actual = (
                                INICIAL_Y - proyectil_y
                        ) / escala

        if altura_actual > altura_maxima:

            altura_maxima = altura_actual

            punto_altura_maxima = (
                proyectil_x,
                proyectil_y
            )

        # Calcular alcance
        alcance_maximo = (
                                 proyectil_x - INICIAL_X
                         ) / escala

        # Detectar impacto
        if proyectil_y >= INICIAL_Y:

            punto_alcance = (
                proyectil_x,
                INICIAL_Y
            )

            proyectil_y = INICIAL_Y

            lanzamiento_activo = False

    # =========================
    # DIBUJAR TRAYECTORIA
    # =========================
    draw_trajectory(
        screen,
        trayectoria,
        AMARILLO
    )

    # =========================
    # ALTURA MÁXIMA
    # =========================
    if punto_altura_maxima:

        pygame.draw.line(
            screen,
            VERDE,
            (
                int(punto_altura_maxima[0]),
                INICIAL_Y
            ),
            (
                int(punto_altura_maxima[0]),
                int(punto_altura_maxima[1])
            ),
            2
        )

        pygame.draw.circle(
            screen,
            VERDE,
            (
                int(punto_altura_maxima[0]),
                int(punto_altura_maxima[1])
            ),
            8
        )

    # =========================
    # ALCANCE MÁXIMO
    # =========================
    if punto_alcance:

        pygame.draw.circle(
            screen,
            NARANJA,
            (
                int(punto_alcance[0]),
                int(punto_alcance[1])
            ),
            10
        )

    # =========================
    # DIBUJAR PROYECTIL
    # =========================
    pygame.draw.circle(
        screen,
        ROJO,
        (
            int(proyectil_x),
            int(proyectil_y)
        ),
        14
    )

    # =========================
    # ACTUALIZAR PANTALLA
    # =========================
    pygame.display.update()

pygame.quit()