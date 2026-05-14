import math

from config import constants

def calcular_escala(
        width, height, start_x, ground_y,
        initial_speed, angle, gravity
):

    angle_rad= math.radians(constants.ANGULO)

    theoretical_range = (
    (constants.VELOCIDAD_INICIAL ** 2)*math.sin(2*angle_rad)
    ) / constants.GRAVEDAD

    theoretical_height = (
    (constants.VELOCIDAD_INICIAL**2)*(math.sin(angle_rad)**2)
    )/(2*constants.GRAVEDAD)

    usable_width = constants.ANCHO_VENTANA - constants.INICIAL_X - 150
    usable_height = constants.INICIAL_Y - 100

    horizontal_scale = usable_width / max(theoretical_height,1)
    vertical_scale = (usable_height) / max(theoretical_height,1)

    scale = min(
        horizontal_scale,
        vertical_scale
    )

    scale *= 0.85
    scale = max(1, min(scale,20))
    return scale

def calculate_velocity(
        initial_speed,
        angle
):
    angle_rad = math.radians(constants.ANGULO)

    velocity_x = (constants.VELOCIDAD_INICIAL*math.cos(constants.ANGULO))
    velocity_y = (constants.VELOCIDAD_INICIAL*math.sin(constants.ANGULO))
    return velocity_x, velocity_y

def calculate_position(
        start_x, ground_y,
        velocity_x, velocity_y,
        gravity, time, scale
):
    proyectile_x = constants.INICIAL_X + (velocity_x*time*scale)
    proyectile_y = constants.INICIAL_Y - (velocity_y*time*scale)-(0.5*constants.GRAVEDAD*(time**2)*scale)
    return proyectile_x, proyectile_y



#dibujar_texto (f"Velocidad Inicial : {constantes.VELOCIDAD_INICIAL} m/s"),
                #constantes.info,constantes.COLOR_NEGRO,20,140)