import pygame

# Inicializamos pygame solo para obtener la info de pantalla
pygame.init()

# RESOLUCIÓN DINÁMICA (Para que se adapte a cualquier PC)
info = pygame.display.Info()
# Restamos un poco al alto para que la barra de tareas no tape la ventana
ALTO_VENTANA = info.current_h - 70
ANCHO_VENTANA = info.current_w

# COLORES (Tu paleta personalizada)
AZUL_CIELO = (135, 206, 235)   # Fondo
VERDE_PASTO = (47, 61, 39)    # Suelo
PANEL_LATERAL = (35, 35, 45)   # UI
PANEL_INTERNO = (50, 50, 65)   # Tarjetas
BORDES = (90, 90, 110)         # Líneas de contorno
BLANCO = (255, 255, 255)
NEGRO = (20, 20, 20)
AMARILLO = (255, 220, 0)       # Trayectoria
ROJO = (255, 70, 70)           # Proyectil
VERDE = (0, 255, 120)          # Altura Máxima
NARANJA = (255, 140, 0)        # Alcance
CYAN = (0, 255, 255)           # Títulos

# CONFIGURACIÓN FÍSICA Y SIMULACIÓN
FPS = 60
GRAVEDAD = 9.81

# Valores por defecto para el inicio
VELOCIDAD_INICIAL = 50
ANGULO = 45
TIEMPO = 0
LANZADOR = False
TRAYECTORIA = []
ESCALA_INICIAL = 10

# POSICIÓN INICIAL DEL LANZAMIENTO
INICIAL_X = 350                # Dejamos espacio para el panel lateral de 320px
INICIAL_Y = ALTO_VENTANA - 120 # Justo encima del suelo