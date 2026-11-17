"""
reserva.py
Clase Reserva: integra cliente, servicio, duración y estado.
Usa try/except/else/finally y encadenamiento de excepciones (raise ... from ...).
"""
from entidades import EntidadBase, Cliente
from excepciones import (
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    ServicioInvalidoError,
    SoftwareFJError,
)
from registro import log
from servicios import Servicio


class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente."""

    # Estados posibles de una reserva
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    FALLIDA = "FALLIDA"

    def __init__(self, cliente, servicio, duracion):
        super().__init__()
        # Parámetros faltantes o de tipo incorrecto
        if cliente is None or servicio is None:
            raise ReservaInvalidaError("Faltan parámetros: cliente y servicio son obligatorios.")
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Tipos inválidos para cliente o servicio.")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self._estado = self.PENDIENTE
        self.costo = None

    @property
    def estado(self):
        """Solo lectura: el estado cambia únicamente con los métodos de la clase."""
        return self._estado

    def confirmar(self):
        """Pasa la reserva de PENDIENTE a CONFIRMADA."""
        if self._estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}."
            )
        # El servicio debe seguir disponible al momento de confirmar
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(f"'{self.servicio.nombre}' no está disponible.")
        self._estado = self.CONFIRMADA
        log.info("Reserva #%s confirmada.", self.id)

    def cancelar(self):
        """Cancela una reserva PENDIENTE o CONFIRMADA."""
        if self._estado in (self.CANCELADA, self.FALLIDA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado {self._estado}."
            )
        self._estado = self.CANCELADA
        log.info("Reserva #%s cancelada.", self.id)

    def procesar(self, impuesto=0.0, descuento=0.0):
        """
        Calcula el costo y confirma la reserva.
        Demuestra try / except / else / finally y encadenamiento con 'from'.
        """
        try:
            # Intentamos calcular el costo (puede lanzar varios errores)
            costo = self.servicio.costo_total(self.duracion, impuesto, descuento)
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(f"'{self.servicio.nombre}' no está disponible.")
        except ServicioInvalidoError as causa:
            # Encadenamiento: la causa original queda ligada al nuevo error
            self._estado = self.FALLIDA
            raise ReservaInvalidaError(
                f"Duración inválida para la reserva #{self.id}."
            ) from causa
        except SoftwareFJError:
            # Otros errores propios del sistema: marcamos fallida y se relanzan
            self._estado = self.FALLIDA
            raise
        else:
            # Solo se ejecuta si NO hubo excepción
            self.costo = costo
            self.confirmar()
            log.info("Reserva #%s procesada. Costo: $%s", self.id, f"{costo:,.2f}")
            return costo
        finally:
            # Siempre se ejecuta: deja constancia del intento
            log.debug("Fin de procesamiento de reserva #%s (estado=%s)", self.id, self._estado)

    def describir(self):
        costo = f"${self.costo:,.2f}" if self.costo is not None else "sin calcular"
        return (f"Reserva #{self.id} [{self._estado}] {self.cliente.nombre} -> "
                f"{self.servicio.nombre}, duración {self.duracion}, costo {costo}")
