import pygame

# IMPORTAR MÓDULOS
from config import constants
from physics.fisicas import (
    calcular_escala,
    calcular_velocidad,
    calcular_posicion
)
from ui.draw import (
    draw_text,
    draw_trajectory,
    draw_background_sprites,
    draw_ground,
    draw_label_with_bg,   # etiquetas con fondo semitransparente
    draw_impact_line      # línea vertical en el punto de impacto
)

# INICIALIZAR PYGAME
pygame.init()

screen = pygame.display.set_mode((constants.ANCHO_VENTANA, constants.ALTO_VENTANA))
pygame.display.set_caption("Simulador de Tiro Parabólico - UPTC")
clock = pygame.time.Clock()

# FUENTES
title_font = pygame.font.SysFont("Arial", 30, bold=True)
info_font  = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 18)

# VARIABLES DE ESTADO
velocidad_inicial = constants.VELOCIDAD_INICIAL
angulo  = constants.ANGULO
escala  = constants.ESCALA_INICIAL
tiempo  = 0
lanzamiento_activo = False

# Velocidades actuales mostradas en el panel (en reposo valen 0)
v_x_actual = 0
v_y_actual = 0

proyectil_x = constants.INICIAL_X
proyectil_y = constants.INICIAL_Y

trayectoria      = []
altura_maxima    = 0
alcance_maximo   = 0
punto_altura_maxima = None
punto_alcance       = None

# BUCLE PRINCIPAL
running = True
while running:

    dt = clock.tick(constants.FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                # Iniciar lanzamiento: resetear estado y calcular escala
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
                # Reiniciar toda la simulación al estado inicial
                lanzamiento_activo = False
                tiempo = 0
                proyectil_x = constants.INICIAL_X
                proyectil_y = constants.INICIAL_Y
                trayectoria.clear()
                punto_altura_maxima = None
                punto_alcance = None

            if event.key == pygame.K_UP:    velocidad_inicial += 2
            if event.key == pygame.K_DOWN:  velocidad_inicial -= 2
            if event.key == pygame.K_RIGHT: angulo += 2
            if event.key == pygame.K_LEFT:  angulo -= 2

    # Limitar rangos de velocidad y ángulo
    velocidad_inicial = max(5, min(velocidad_inicial, 100))
    angulo = max(5, min(angulo, 85))
    v_x_inicial, v_y_inicial = calcular_velocidad(velocidad_inicial, angulo)

    # LÓGICA DE MOVIMIENTO
    if lanzamiento_activo:
        tiempo += dt * 2
        proyectil_x, proyectil_y = calcular_posicion(
            constants.INICIAL_X, constants.INICIAL_Y,
            v_x_inicial, v_y_inicial, constants.GRAVEDAD, tiempo, escala
        )

        # Velocidades instantáneas durante el vuelo
        v_x_actual = v_x_inicial
        v_y_actual = v_y_inicial - (constants.GRAVEDAD * tiempo)

        if proyectil_y <= constants.INICIAL_Y:
            trayectoria.append((proyectil_x, proyectil_y))

            # Registrar altura máxima alcanzada
            alt_actual = (constants.INICIAL_Y - proyectil_y) / escala
            if alt_actual > altura_maxima:
                altura_maxima = alt_actual
                punto_altura_maxima = (proyectil_x, proyectil_y)

            alcance_maximo = (proyectil_x - constants.INICIAL_X) / escala
        else:
            # Impacto con el suelo: detener simulación
            punto_alcance = (proyectil_x, constants.INICIAL_Y)
            proyectil_y   = constants.INICIAL_Y
            v_x_actual    = 0
            v_y_actual    = 0
            lanzamiento_activo = False
    else:
        # En reposo las velocidades son cero
        v_x_actual = 0
        v_y_actual = 0

    # RENDERIZADO (DIBUJO)
    # El orden importa: lo que se dibuja después queda encima.
    # 1. Fondo base del panel lateral (color sólido oscuro)
    screen.fill(constants.PANEL_LATERAL)

    # 2. Sprites de fondo: cielo → montañas → árboles/pasto (en ese orden dentro de la función)
    draw_background_sprites(screen)

    # 3. Rectángulo de suelo sólido (el pasto.png se dibuja encima dentro de draw_background_sprites)
    draw_ground(screen, constants.VERDE_PASTO, constants.ANCHO_VENTANA, constants.INICIAL_Y)

    # 4. Panel lateral oscuro (se redibuja encima del fondo para que los sprites no lo tapen)
    pygame.draw.rect(screen, constants.PANEL_LATERAL, (0, 0, 320, constants.ALTO_VENTANA))
    draw_text(screen, "SIMULADOR FÍSICA", title_font, constants.CYAN, 20, 20)

    # 5. Recuadro de datos de la simulación
    pygame.draw.rect(screen, constants.PANEL_INTERNO, (15, 70, 290, 320), border_radius=12)
    pygame.draw.rect(screen, constants.BORDES,        (15, 70, 290, 320), 2, border_radius=12)

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

    # 6. Recuadro de controles
    pygame.draw.rect(screen, constants.PANEL_INTERNO, (15, 410, 290, 160), border_radius=12)
    pygame.draw.rect(screen, constants.BORDES,        (15, 410, 290, 160), 2, border_radius=12)

    draw_text(screen, "CONTROLES", info_font, constants.CYAN, 30, 425)
    controles = [
        "[ESPACIO] Lanzar Proyectil",
        "[R] Reiniciar Simulación",
        "[↑ / ↓] Ajustar Velocidad",
        "[← / →] Ajustar Ángulo"
    ]
    for i, inst in enumerate(controles):
        draw_text(screen, inst, small_font, constants.BLANCO, 30, 465 + (i * 22))

    # 7. Trayectoria del proyectil (puntos amarillos)
    draw_trajectory(screen, trayectoria, constants.AMARILLO)

    # 8. Marcador de altura máxima con etiqueta legible
    if punto_altura_maxima:
        pygame.draw.circle(
            screen, constants.VERDE,
            (int(punto_altura_maxima[0]), int(punto_altura_maxima[1])), 6
        )
        #usamos draw_label_with_bg en lugar de draw_text para que
        #la etiqueta sea legible sobre el fondo de montañas
        draw_label_with_bg(
            screen,
            f"Altura máxima: {round(altura_maxima, 1)}m",
            small_font,
            punto_altura_maxima[0] - 15,
            punto_altura_maxima[1] - 28   # Un poco más arriba para no tapar el punto
        )

    # 9. Marcador de alcance máximo con línea vertical y etiqueta legible
    if punto_alcance:
    # línea vertical que baja desde 30px arriba del suelo hasta el impacto
        draw_impact_line(screen, punto_alcance)

        pygame.draw.circle(
            screen, constants.NARANJA,
            (int(punto_alcance[0]), int(punto_alcance[1])), 10
        )
        #etiqueta con fondo semitransparente. Corregido "máxima" → "máximo"
        draw_label_with_bg(
            screen,
            f"Alcance máximo: {round(alcance_maximo, 1)}m",  # <-- typo corregido
            small_font,
            punto_alcance[0] - 40,
            punto_alcance[1] + 15
        )

    # 10. Proyectil (se dibuja al final para que quede siempre encima de todo)
    pygame.draw.circle(screen, constants.ROJO, (int(proyectil_x), int(proyectil_y)), 14)

    pygame.display.update()

pygame.quit()