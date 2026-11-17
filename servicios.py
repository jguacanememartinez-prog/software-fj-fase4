"""
servicios.py
Clase abstracta Servicio y tres servicios especializados (herencia + polimorfismo).
Incluye métodos sobrecargados para el cálculo de costos.
"""
from abc import abstractmethod

from entidades import EntidadBase
from excepciones import (
    CalculoInconsistenteError,
    ServicioInvalidoError,
)
from registro import log


class Servicio(EntidadBase):
    """Clase abstracta: define lo que todo servicio de Software FJ debe ofrecer."""

    def __init__(self, nombre, tarifa_base, disponible=True):
        super().__init__()
        # Validamos antes de guardar los datos
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio necesita un nombre.")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise ServicioInvalidoError(
                f"La tarifa base debe ser un número positivo, recibido: {tarifa_base!r}"
            )
        self.nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self.disponible = disponible

    @property
    def tarifa_base(self):
        """Solo lectura: la tarifa se define al crear el servicio."""
        return self._tarifa_base

    # ---- métodos abstractos que cada hijo debe sobrescribir ----
    @abstractmethod
    def calcular_costo(self, duracion):
        """Costo base (sin impuestos ni descuentos) según la duración."""

    @abstractmethod
    def validar_parametros(self, duracion):
        """Lanza ServicioInvalidoError si los parámetros no sirven."""

    # ---- método sobrecargado: varias formas de llamarlo ----
    def costo_total(self, duracion, impuesto=0.0, descuento=0.0):
        """
        Sobrecarga mediante parámetros opcionales:
          costo_total(2)                    -> costo base
          costo_total(2, 0.19)              -> con IVA
          costo_total(2, 0.19, 0.10)        -> con IVA y 10 % de descuento
          costo_total(2, descuento=0.10)    -> solo descuento
        """
        # Validamos la lógica de los porcentajes
        if not 0 <= impuesto <= 1:
            raise CalculoInconsistenteError(f"Impuesto fuera de rango: {impuesto}")
        if not 0 <= descuento < 1:
            raise CalculoInconsistenteError(f"Descuento fuera de rango: {descuento}")
        self.validar_parametros(duracion)
        base = self.calcular_costo(duracion)
        total = base * (1 - descuento) * (1 + impuesto)
        # Un costo no positivo indica un cálculo inconsistente
        if total <= 0:
            raise CalculoInconsistenteError("El costo total resultó no positivo.")
        return round(total, 2)

    def describir(self):
        estado = "disponible" if self.disponible else "NO disponible"
        return f"{self.__class__.__name__} '{self.nombre}' ({estado})"


class ReservaSala(Servicio):
    """Reserva de salas: se cobra por hora y con recargo según capacidad."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad debe ser un entero positivo.")
        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        # Las salas se reservan entre 1 y 12 horas
        if not isinstance(duracion, (int, float)) or not 1 <= duracion <= 12:
            raise ServicioInvalidoError("Las salas se reservan entre 1 y 12 horas.")

    def calcular_costo(self, duracion):
        costo = self.tarifa_base * duracion
        # Recargo del 15 % si la sala es grande (más de 20 personas)
        if self.capacidad > 20:
            costo *= 1.15
        return costo

    def describir(self):
        return super().describir() + f" - capacidad {self.capacidad} personas"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: se cobra por equipo y por día, más un seguro."""

    SEGURO = 0.05  # 5 % del valor como seguro

    def __init__(self, nombre, tarifa_dia, cantidad, disponible=True):
        super().__init__(nombre, tarifa_dia, disponible)
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ServicioInvalidoError("La cantidad de equipos debe ser positiva.")
        self.cantidad = cantidad

    def validar_parametros(self, duracion):
        # Los equipos se alquilan por días enteros, entre 1 y 30
        if not isinstance(duracion, int) or not 1 <= duracion <= 30:
            raise ServicioInvalidoError("Los equipos se alquilan de 1 a 30 días enteros.")

    def calcular_costo(self, duracion):
        return self.tarifa_base * self.cantidad * duracion * (1 + self.SEGURO)

    def describir(self):
        return super().describir() + f" - {self.cantidad} equipo(s), seguro {self.SEGURO:.0%}"


class AsesoriaEspecializada(Servicio):
    """Asesoría: se cobra por hora y según el nivel del asesor."""

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre, tarifa_hora, nivel, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if nivel not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel inválido: {nivel!r}. Use {list(self.NIVELES)}"
            )
        self.nivel = nivel

    def validar_parametros(self, duracion):
        # Asesorías de 1 a 8 horas
        if not isinstance(duracion, (int, float)) or not 1 <= duracion <= 8:
            raise ServicioInvalidoError("Las asesorías duran entre 1 y 8 horas.")

    def calcular_costo(self, duracion):
        return self.tarifa_base * duracion * self.NIVELES[self.nivel]

    def describir(self):
        return super().describir() + f" - nivel {self.nivel}"
