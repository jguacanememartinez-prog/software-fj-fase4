"""
excepciones.py
Excepciones personalizadas del sistema Software FJ.
Todas heredan de SoftwareFJError para poder capturarlas de forma general o específica.
"""


class SoftwareFJError(Exception):
    """Excepción base del sistema: de ella heredan todas las demás."""

    def __init__(self, mensaje, codigo="FJ-000"):
        # Llamamos al constructor de Exception con el mensaje
        super().__init__(mensaje)
        # Guardamos un código de error para facilitar la lectura del log
        self.codigo = codigo

    def __str__(self):
        # Formato uniforme: [CODIGO] mensaje
        return f"[{self.codigo}] {super().__str__()}"


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no cumplen las validaciones."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-101")


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando los parámetros de un servicio son inválidos."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-201")


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta usar un servicio que no está disponible."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-202")


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no puede crearse o procesarse."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-301")


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se pide una operación que el estado actual no permite."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-302")


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos produce valores inconsistentes."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-401")
