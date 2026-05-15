import math
# Importamos el módulo de constantes para acceder a los valores de configuración
from config import constants

def calcular_escala(width, height, start_x, ground_y, initial_speed, angle, gravity):
    """Calcula una escala dinámica para que la trayectoria quepa en la pantalla."""
    angle_rad = math.radians(angle)

    # Ecuaciones físicas del alcance (R) y altura máxima (H)
    theoretical_range = ((initial_speed ** 2) * math.sin(2 * angle_rad)) / gravity
    theoretical_height = ((initial_speed ** 2) * (math.sin(angle_rad) ** 2)) / (2 * gravity)

    # Espacio disponible en la interfaz
    usable_width = width - start_x - 150
    usable_height = ground_y - 100

    # Relacionar correctamente los ejes con sus magnitudes físicas
    horizontal_scale = usable_width / max(theoretical_range, 1)
    vertical_scale = usable_height / max(theoretical_height, 1)

    # Seleccionar la escala más restrictiva para asegurar visibilidad total
    scale = min(horizontal_scale, vertical_scale)
    return max(1, min(scale * 0.85, 20))

def calcular_velocidad(initial_speed, angle):
    """Descompone la velocidad inicial en sus componentes X e Y."""
    angle_rad = math.radians(angle)
    velocity_x = initial_speed * math.cos(angle_rad)
    velocity_y = initial_speed * math.sin(angle_rad)
    return velocity_x, velocity_y

def calcular_posicion(start_x, ground_y, velocity_x, velocity_y, gravity, time, scale):
    """Calcula las coordenadas (x, y) en pixeles para un tiempo 't' dado."""
    # Movimiento horizontal (MRU)
    proyectile_x = start_x + (velocity_x * time * scale)
    # Movimiento vertical (MRUV) - Se resta de ground_y porque el eje Y en Pygame baja
    proyectile_y = ground_y - (velocity_y * time * scale - 0.5 * gravity * (time**2) * scale)
    return proyectile_x, proyectile_y