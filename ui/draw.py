import pygame
from config import constants

# =============================================================
# PAQUETE: ui/draw.py
# Este módulo contiene todas las funciones de dibujo/renderizado
# de la interfaz visual del simulador.
# =============================================================

# Variables globales para los sprites del fondo.
# Se declaran vacías aquí porque pygame aún no está listo al importar.
# Se llenan la primera vez que se llama a cargar_sprites().
cielo    = None   # Imagen de fondo con cielo y nubes
montanas = None   # Imagen de montañas con transparencia
suelo    = None   # NUEVO: imagen de árboles y pasto con transparencia


def cargar_sprites():
    """
    Carga y escala todas las imágenes de fondo UNA SOLA VEZ.
    Se llama desde draw_background_sprites() antes de dibujar,
    así nos aseguramos de que pygame ya esté inicializado.
    """
    global cielo, montanas, suelo

    # Solo cargamos si todavía no se han cargado (evita recargar cada frame)
    if cielo is None:

        # --- CAPA 1: Cielo con nubes ---
        # Se escala para ocupar exactamente el área de juego (sin el panel lateral)
        cielo = pygame.image.load("nubes.png").convert_alpha()
        cielo = pygame.transform.scale(
            cielo, (constants.ANCHO_VENTANA - 320, constants.ALTO_VENTANA)
        )

        # --- CAPA 2: Montañas de fondo ---
        # También se escala al área de juego completa
        montanas = pygame.image.load("fondo.png").convert_alpha()
        montanas = pygame.transform.scale(
            montanas, (constants.ANCHO_VENTANA - 320, constants.ALTO_VENTANA)
        )

        # --- CAPA 3: Árboles y pasto (pasto.png) ---
        # NUEVO: Esta imagen tiene fondo negro que necesitamos eliminar.
        # set_colorkey le dice a pygame que trate el negro puro (0,0,0)
        # como si fuera transparente al momento de dibujarla.
        suelo = pygame.image.load("pasto.png").convert_alpha()
        suelo.set_colorkey((0, 0, 0))  # El negro se vuelve transparente

        # La escalamos al mismo ancho del área de juego.
        # El alto lo dejamos proporcional para no deformar los árboles.
        ancho_juego = constants.ANCHO_VENTANA - 320
        alto_original = suelo.get_height()
        ancho_original = suelo.get_width()
        # Calculamos el alto proporcional según el nuevo ancho
        alto_proporcional = int(alto_original * ancho_juego / ancho_original)
        suelo = pygame.transform.scale(suelo, (ancho_juego, alto_proporcional))


def draw_background_sprites(screen):
    """
    Dibuja las tres capas del fondo en orden (de atrás hacia adelante):
      1. Cielo/nubes  (la más lejana)
      2. Montañas     (capa media)
      3. Árboles/pasto (la más cercana al suelo)
    Todas se dibujan a partir de x=320 para no tapar el panel lateral.
    """
    cargar_sprites()  # Garantiza que las imágenes estén listas

    # Capa 1: cielo — cubre toda el área de juego desde arriba
    screen.blit(cielo, (320, 0))

    # Capa 2: montañas — se superpone sobre el cielo
    screen.blit(montanas, (320, 0))

    # NUEVO — Capa 3: árboles/pasto
    # La posicionamos alineada con el suelo (INICIAL_Y).
    # Restamos el alto de la imagen para que su borde inferior quede
    # justo en la línea del suelo, simulando que los árboles "crecen" desde ahí.
    pos_y_suelo = constants.INICIAL_Y - suelo.get_height() + 40
    # El +40 es un ajuste fino para que la base de los árboles quede
    # ligeramente enterrada en el rectángulo de pasto, sin espacio negro visible.
    screen.blit(suelo, (320, pos_y_suelo))


def draw_text(ventana, text, font, color, x, y):
    """
    Dibuja texto simple sin fondo.
    Usada para el panel lateral donde el fondo oscuro ya da contraste suficiente.
    """
    render = font.render(text, True, color)
    ventana.blit(render, (x, y))


def draw_label_with_bg(screen, text, font, x, y):
    """
    NUEVO: Dibuja una etiqueta de texto con un rectángulo blanco semitransparente
    detrás, para que sea legible aunque caiga sobre el fondo de montañas.

    Parámetros:
      screen : superficie de pygame donde se dibuja
      text   : cadena de texto a mostrar
      font   : fuente de pygame
      x, y   : posición de la esquina superior izquierda del texto
    """
    # Renderizamos el texto en negro para máximo contraste con el fondo blanco
    texto_surface = font.render(text, True, constants.NEGRO)

    # Creamos una superficie con canal alfa (transparencia) para el fondo
    # Le damos 8px de margen horizontal y 4px vertical alrededor del texto
    padding_x = 8
    padding_y = 4
    bg_ancho = texto_surface.get_width() + padding_x * 2
    bg_alto  = texto_surface.get_height() + padding_y * 2
    bg_surface = pygame.Surface((bg_ancho, bg_alto), pygame.SRCALPHA)

    # Rellenamos con blanco semitransparente: (R, G, B, Alpha)
    # Alpha 170 de 255 = ~67% opaco, suficiente para leer sin tapar el fondo
    bg_surface.fill((255, 255, 255, 170))

    # Dibujamos primero el fondo, luego el texto encima
    screen.blit(bg_surface, (x - padding_x, y - padding_y))
    screen.blit(texto_surface, (x, y))


def draw_trajectory(screen, trajectory, color):
    """
    Dibuja la trayectoria del proyectil como una serie de círculos pequeños.
    Cada punto es una posición registrada durante el vuelo.
    """
    for point in trajectory:
        pygame.draw.circle(screen, color, (int(point[0]), int(point[1])), 4)


def draw_impact_line(screen, punto_alcance):
    """
    NUEVO: Dibuja una línea vertical desde el punto de impacto hasta el suelo.
    Esto hace más claro visualmente dónde exactamente cayó el proyectil,
    especialmente cuando el marcador circular queda sobre la línea del suelo.

    Parámetros:
      screen        : superficie de pygame
      punto_alcance : tupla (x, y) con la posición del impacto
    """
    x_impacto = int(punto_alcance[0])
    y_impacto = int(punto_alcance[1])

    # Dibujamos la línea desde 30px arriba del impacto hasta el punto mismo
    # en color naranja para que coincida con el círculo de alcance
    pygame.draw.line(
        screen,
        constants.NARANJA,          # Color: naranja (igual que el marcador)
        (x_impacto, y_impacto - 30),  # Punto superior de la línea
        (x_impacto, y_impacto),       # Punto inferior (el suelo)
        2                             # Grosor de 2 píxeles
    )


def draw_ground(screen, color, width, ground_y):
    """
    Dibuja el rectángulo de color sólido que representa el suelo.
    Se dibuja desde x=320 hacia la derecha para no pisar el panel lateral.
    Las capas de pasto/árboles se dibujan encima en draw_background_sprites().
    """
    pygame.draw.rect(screen, color, (320, ground_y, width, 120))


# def draw_text(ventana, text, font, color, x, y):
#     render = font.render(text, True, color)
#     ventana.blit(render, (x, y))
#
# def draw_trajectory(screen, trajectory, color):
#     # Dibujamos círculos pequeños para la trayectoria
#     for point in trajectory:
#         pygame.draw.circle(screen, color, (int(point[0]), int(point[1])), 4)
#
# def draw_ground(screen, color, width, ground_y):
#       #El suelo ahora se dibuja desde el panel lateral hacia la derecha
#     pygame.draw.rect(screen, color, (320, ground_y, width, 120))

