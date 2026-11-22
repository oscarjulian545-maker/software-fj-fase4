"""Módulo de excepciones personalizadas para el sistema de Software FJ."""  # Documenta el propósito del archivo


class ErrorSoftwareFJ(Exception):
    """Excepción base del sistema de gestión de Software FJ."""  # Define la excepción raíz del dominio

    def __init__(self, mensaje: str, detalle: str = "") -> None:
        """Inicializa la excepción con un mensaje principal y un detalle opcional."""  # Documenta el constructor
        super().__init__(mensaje)  # Pasa el mensaje principal a Exception
        self.mensaje = mensaje  # Almacena el mensaje de error
        self.detalle = detalle  # Almacena información adicional para diagnóstico


class ErrorValidacionEntidad(ErrorSoftwareFJ):
    """Se lanza cuando los datos o parámetros de una entidad son inválidos o faltan."""  # Excepción por validación


class ErrorServicioNoDisponible(ErrorSoftwareFJ):
    """Se lanza cuando se intenta usar o reservar un servicio que no está disponible."""  # Excepción de disponibilidad


class ErrorReservaInvalida(ErrorSoftwareFJ):
    """Se lanza cuando una reserva presenta estados, duraciones o transiciones incorrectas."""  # Excepción de reserva


class ErrorCalculoFinanciero(ErrorSoftwareFJ):
    """Se lanza cuando ocurre un cálculo inconsistente de costos, descuentos o impuestos."""  # Excepción de cálculo